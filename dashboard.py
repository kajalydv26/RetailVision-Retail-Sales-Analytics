import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import FuncFormatter


# =====================================================
# CONFIGURATION
# =====================================================

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "sales_data.csv"

BG = "#F3F6FB"
SIDEBAR = "#172554"
CARD = "#FFFFFF"
BLUE = "#3B82F6"
GREEN = "#16A34A"
ORANGE = "#F59E0B"
PURPLE = "#8B5CF6"
TEXT = "#1E293B"
MUTED = "#64748B"
BORDER = "#E2E8F0"


# =====================================================
# LOAD AND PREPARE KAGGLE DATA
# =====================================================

def load_data():
    # Support both the renamed CSV and original Kaggle filename.
    possible_files = [
        DATA_FILE,
        BASE_DIR / "Sample - Superstore.csv",
        BASE_DIR / "Sample-Superstore.csv"
    ]

    csv_file = next(
        (file for file in possible_files if file.exists()),
        None
    )

    if csv_file is None:
        raise FileNotFoundError(
            "Sales CSV file was not found.\n\n"
            "Place sales_data.csv in the same folder as dashboard.py."
        )

    # Read a larger CSV without relying on a small sample.
    errors = []

    for encoding in ("utf-8-sig", "latin1"):
        try:
            data = pd.read_csv(
                csv_file,
                encoding=encoding,
                sep=None,
                engine="python",
                on_bad_lines="warn"
            )
            break
        except Exception as error:
            errors.append(str(error))
    else:
        raise ValueError("\n".join(errors))

    # Clean column names.
    data.columns = [
        str(column).strip().replace("\ufeff", "")
        for column in data.columns
    ]

    # Match columns without depending on capitalization.
    column_lookup = {
        column.strip().lower(): column
        for column in data.columns
    }

    aliases = {
        "Order ID": ["Order ID", "Order_ID", "OrderID"],
        "Order Date": ["Order Date", "Date", "Order_Date"],
        "Product Name": ["Product Name", "Product", "Product_Name"],
        "Category": ["Category"],
        "Sub-Category": ["Sub-Category", "Sub Category"],
        "Region": ["Region"],
        "Sales": ["Sales", "Revenue"],
        "Quantity": ["Quantity", "Qty"],
        "Profit": ["Profit"]
    }

    rename_map = {}

    for standard_name, possible_names in aliases.items():
        for possible_name in possible_names:
            original_name = column_lookup.get(
                possible_name.lower()
            )

            if original_name is not None:
                rename_map[original_name] = standard_name
                break

    data = data.rename(columns=rename_map)

    required_columns = [
        "Order ID",
        "Order Date",
        "Category",
        "Region",
        "Sales",
        "Quantity"
    ]

    missing = [
        column for column in required_columns
        if column not in data.columns
    ]

    if missing:
        raise ValueError(
            f"Missing columns: {missing}\n\n"
            f"Columns found in CSV:\n{list(data.columns)}"
        )

    # Convert values to correct data types.
    data["Order Date"] = pd.to_datetime(
        data["Order Date"],
        errors="coerce"
    )

    data["Sales"] = pd.to_numeric(
        data["Sales"], errors="coerce"
    )

    data["Quantity"] = pd.to_numeric(
        data["Quantity"], errors="coerce"
    )

    if "Profit" in data.columns:
        data["Profit"] = pd.to_numeric(
            data["Profit"], errors="coerce"
        )
    else:
        data["Profit"] = 0

    # Remove invalid rows.
    data = data.dropna(
        subset=[
            "Order Date",
            "Sales",
            "Quantity",
            "Order ID",
            "Category",
            "Region"
        ]
    ).copy()

    if data.empty:
        raise ValueError("No valid sales records were found.")

    # Create chronological month labels.
    data["Month"] = data["Order Date"].dt.to_period("M")

    data["Month Label"] = data["Order Date"].dt.strftime(
        "%b %Y"
    )

    if "Product Name" not in data.columns:
        data["Product Name"] = "Unknown Product"

    if "Sub-Category" not in data.columns:
        data["Sub-Category"] = data["Category"]

    return data


try:
    df = load_data()

except Exception as error:
    error_root = tk.Tk()
    error_root.withdraw()

    messagebox.showerror(
        "Data Loading Error",
        str(error)
    )

    error_root.destroy()
    raise SystemExit


# =====================================================
# MAIN WINDOW
# =====================================================

root = tk.Tk()
root.title("RETAILVISION")
root.geometry("1280x850")
root.minsize(1000, 700)
root.configure(bg=BG)


# =====================================================
# HELPER FUNCTIONS
# =====================================================

def money(value):
    return f"{value:,.0f}"


def currency_axis(value, position):
    return f"{value:,.0f}"


def create_label(parent, text, size=10, color=TEXT,
                 bold=False, bg=CARD):
    return tk.Label(
        parent,
        text=text,
        font=(
            "Segoe UI",
            size,
            "bold" if bold else "normal"
        ),
        fg=color,
        bg=bg
    )


# =====================================================
# HEADER
# =====================================================

header = tk.Frame(root, bg=SIDEBAR, height=120)
header.pack(fill="x")
header.pack_propagate(False)

header_left = tk.Frame(header, bg=SIDEBAR)
header_left.pack(side="left", padx=28, pady=18)

tk.Label(
    header_left,
    text="RETAILVISION",
    font=("Segoe UI", 25, "bold"),
    fg="white",
    bg=SIDEBAR
).pack(anchor="w")

tk.Label(
    header_left,
    text="Retail Sales Analytics | Business Intelligence Dashboard",
    font=("Segoe UI", 10),
    fg="#BFDBFE",
    bg=SIDEBAR
).pack(anchor="w", pady=(6, 0))

header_right = tk.Frame(header, bg=SIDEBAR)
header_right.pack(side="right", padx=25)

tk.Label(
    header_right,
    text=f"{len(df):,} SALES RECORDS",
    font=("Segoe UI", 10, "bold"),
    fg="white",
    bg="#334155",
    padx=14,
    pady=9
).pack()


# =====================================================
# FILTER BAR
# =====================================================

filter_bar = tk.Frame(root, bg=BG)
filter_bar.pack(fill="x", padx=22, pady=(15, 8))

create_label(
    filter_bar,
    "FILTER DATA",
    size=10,
    color=MUTED,
    bold=True,
    bg=BG
).pack(side="left", padx=(0, 15))


region_var = tk.StringVar(value="All Regions")
category_var = tk.StringVar(value="All Categories")

region_options = ["All Regions"] + sorted(
    df["Region"].astype(str).unique().tolist()
)

category_options = ["All Categories"] + sorted(
    df["Category"].astype(str).unique().tolist()
)

region_box = ttk.Combobox(
    filter_bar,
    textvariable=region_var,
    values=region_options,
    state="readonly",
    width=19
)
region_box.pack(side="left", padx=5)

category_box = ttk.Combobox(
    filter_bar,
    textvariable=category_var,
    values=category_options,
    state="readonly",
    width=21
)
category_box.pack(side="left", padx=5)

reset_button = tk.Button(
    filter_bar,
    text="Reset Filters",
    command=lambda: reset_filters(),
    bg=BLUE,
    fg="white",
    activebackground="#2563EB",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    font=("Segoe UI", 9, "bold"),
    padx=13,
    pady=7
)
reset_button.pack(side="left", padx=10)


# =====================================================
# KPI CARDS
# =====================================================

kpi_frame = tk.Frame(root, bg=BG)
kpi_frame.pack(fill="x", padx=17, pady=8)

kpi_definitions = [
    ("TOTAL SALES", BLUE),
    ("TOTAL ORDERS", GREEN),
    ("UNITS SOLD", ORANGE),
    ("TOTAL PROFIT", PURPLE)
]

kpi_values = []

for title, accent in kpi_definitions:
    card = tk.Frame(
        kpi_frame,
        bg=CARD,
        highlightbackground=BORDER,
        highlightthickness=1
    )
    card.pack(
        side="left",
        fill="both",
        expand=True,
        padx=5
    )

    tk.Frame(
        card,
        bg=accent,
        height=4
    ).pack(fill="x")

    create_label(
        card,
        title,
        size=9,
        color=MUTED,
        bold=True
    ).pack(anchor="w", padx=15, pady=(13, 4))

    value_label = create_label(
        card,
        "0",
        size=19,
        color=accent,
        bold=True
    )
    value_label.pack(anchor="w", padx=15, pady=(0, 14))

    kpi_values.append(value_label)


# =====================================================
# BUSINESS INSIGHTS
# =====================================================

insight_frame = tk.Frame(
    root,
    bg=CARD,
    highlightbackground=BORDER,
    highlightthickness=1
)
insight_frame.pack(fill="x", padx=22, pady=(5, 10))

insight_label = create_label(
    insight_frame,
    "",
    size=10,
    color=TEXT,
    bold=True
)
insight_label.pack(
    fill="x",
    padx=15,
    pady=12,
    anchor="w"
)


# =====================================================
# CHART LAYOUT
# =====================================================

chart_area = tk.Frame(root, bg=BG)
chart_area.pack(
    fill="both",
    expand=True,
    padx=17,
    pady=(0, 12)
)

chart_area.grid_columnconfigure(0, weight=1)
chart_area.grid_columnconfigure(1, weight=1)
chart_area.grid_rowconfigure(0, weight=1)
chart_area.grid_rowconfigure(1, weight=1)


def make_chart_card(row, column, title):
    card = tk.Frame(
        chart_area,
        bg=CARD,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    card.grid(
        row=row,
        column=column,
        sticky="nsew",
        padx=5,
        pady=5
    )

    title_label = create_label(
        card,
        title,
        size=11,
        bold=True
    )
    title_label.pack(pady=(9, 0))

    figure, axis = plt.subplots(
        figsize=(5.4, 2.65),
        dpi=85
    )

    figure.patch.set_facecolor(CARD)
    axis.set_facecolor(CARD)

    figure.subplots_adjust(
        left=0.14,
        right=0.97,
        top=0.86,
        bottom=0.22
    )

    canvas = FigureCanvasTkAgg(
        figure,
        master=card
    )

    canvas.get_tk_widget().pack(
        fill="both",
        expand=True,
        padx=5,
        pady=3
    )

    return figure, axis, canvas


fig_month, ax_month, canvas_month = make_chart_card(
    0, 0, "Monthly Sales Trend"
)

fig_category, ax_category, canvas_category = make_chart_card(
    0, 1, "Sales by Category"
)

fig_region, ax_region, canvas_region = make_chart_card(
    1, 0, "Sales by Region"
)

fig_share, ax_share, canvas_share = make_chart_card(
    1, 1, "Category Sales Distribution"
)


# =====================================================
# FILTERING AND CHART UPDATES
# =====================================================

def get_filtered_data():
    filtered = df.copy()

    selected_region = region_var.get()
    selected_category = category_var.get()

    if selected_region != "All Regions":
        filtered = filtered[
            filtered["Region"].astype(str) == selected_region
        ]

    if selected_category != "All Categories":
        filtered = filtered[
            filtered["Category"].astype(str) == selected_category
        ]

    return filtered


def update_dashboard(*args):
    data = get_filtered_data()

    # KPI calculations
    total_sales = data["Sales"].sum()
    total_orders = data["Order ID"].nunique()
    total_units = data["Quantity"].sum()
    total_profit = data["Profit"].sum()

    kpi_values[0].config(text=f"${money(total_sales)}")
    kpi_values[1].config(text=f"{total_orders:,}")
    kpi_values[2].config(text=f"{total_units:,.0f}")
    kpi_values[3].config(text=f"${money(total_profit)}")

    # Top category and region
    category_totals = data.groupby("Category")["Sales"].sum()
    region_totals = data.groupby("Region")["Sales"].sum()

    top_category = (
        str(category_totals.idxmax())
        if not category_totals.empty else "N/A"
    )

    top_region = (
        str(region_totals.idxmax())
        if not region_totals.empty else "N/A"
    )

    insight_label.config(
        text=(
            f"TOP CATEGORY: {top_category}     |     "
            f"TOP REGION: {top_region}     |     "
            f"FILTERED RECORDS: {len(data):,}"
        )
    )

    # Clear previous charts
    axes = [
        ax_month,
        ax_category,
        ax_region,
        ax_share
    ]

    for axis in axes:
        axis.clear()
        axis.set_facecolor(CARD)
        axis.tick_params(
            labelsize=8,
            colors=MUTED
        )

        for spine in axis.spines.values():
            spine.set_color(BORDER)

    # 1. MONTHLY SALES TREND
    if not data.empty:
        monthly = (
            data.groupby("Month")["Sales"]
            .sum()
            .sort_index()
        )

        month_labels = [
            period.strftime("%b %Y")
            for period in monthly.index
        ]

        ax_month.plot(
            range(len(monthly)),
            monthly.to_numpy(),
            color=BLUE,
            linewidth=2.5,
            marker="o",
            markersize=5
        )

        ax_month.fill_between(
            range(len(monthly)),
            monthly.to_numpy(),
            color=BLUE,
            alpha=0.12
        )

        ax_month.set_xticks(range(len(monthly)))
        ax_month.set_xticklabels(
            month_labels,
            rotation=30,
            ha="right"
        )

        ax_month.set_ylabel("Sales ($)", fontsize=8)
        ax_month.yaxis.set_major_formatter(
            FuncFormatter(currency_axis)
        )
        ax_month.grid(
            axis="y",
            linestyle="--",
            alpha=0.25
        )

    else:
        ax_month.text(
            0.5, 0.5, "No data available",
            ha="center", va="center",
            transform=ax_month.transAxes
        )

    # 2. SALES BY CATEGORY
    category_sales = (
        data.groupby("Category")["Sales"]
        .sum()
        .sort_values()
    )

    if not category_sales.empty:
        bars = ax_category.bar(
            category_sales.index.astype(str),
            category_sales.to_numpy(),
            color=[BLUE, GREEN, ORANGE, PURPLE][:len(category_sales)]
        )

        ax_category.set_ylabel("Sales ($)", fontsize=8)
        ax_category.yaxis.set_major_formatter(
            FuncFormatter(currency_axis)
        )

        ax_category.tick_params(
            axis="x",
            rotation=15
        )

        ax_category.grid(
            axis="y",
            linestyle="--",
            alpha=0.25
        )

        for bar in bars:
            height = bar.get_height()
            ax_category.annotate(
                f"${height:,.0f}",
                (
                    bar.get_x() + bar.get_width() / 2,
                    height
                ),
                ha="center",
                va="bottom",
                fontsize=7,
                xytext=(0, 3),
                textcoords="offset points"
            )
    else:
        ax_category.text(
            0.5, 0.5, "No data available",
            ha="center", va="center",
            transform=ax_category.transAxes
        )

    # 3. SALES BY REGION
    region_sales = (
        data.groupby("Region")["Sales"]
        .sum()
        .sort_values()
    )

    if not region_sales.empty:
        bars = ax_region.barh(
            region_sales.index.astype(str),
            region_sales.to_numpy(),
            color=GREEN
        )

        ax_region.set_xlabel("Sales ($)", fontsize=8)
        ax_region.xaxis.set_major_formatter(
            FuncFormatter(currency_axis)
        )

        ax_region.grid(
            axis="x",
            linestyle="--",
            alpha=0.25
        )

        for bar in bars:
            width = bar.get_width()

            ax_region.annotate(
                f"${width:,.0f}",
                (width, bar.get_y() + bar.get_height() / 2),
                xytext=(4, 0),
                textcoords="offset points",
                va="center",
                fontsize=7
            )
    else:
        ax_region.text(
            0.5, 0.5, "No data available",
            ha="center", va="center",
            transform=ax_region.transAxes
        )

    # 4. CATEGORY SALES DISTRIBUTION
    share = data.groupby("Category")["Sales"].sum()
    share = share[share > 0]

    if not share.empty:
        ax_share.pie(
            share.to_numpy(),
            labels=share.index.astype(str),
            autopct="%1.1f%%",
            startangle=90,
            colors=[
                BLUE,
                ORANGE,
                GREEN,
                PURPLE
            ][:len(share)],
            textprops={"fontsize": 8},
            wedgeprops={
                "linewidth": 1,
                "edgecolor": "white"
            }
        )

        ax_share.axis("equal")
    else:
        ax_share.text(
            0.5, 0.5, "No positive sales to display",
            ha="center", va="center",
            transform=ax_share.transAxes
        )

    # Refresh the charts
    for figure, canvas in [
        (fig_month, canvas_month),
        (fig_category, canvas_category),
        (fig_region, canvas_region),
        (fig_share, canvas_share)
    ]:
        figure.tight_layout()
        canvas.draw_idle()


def reset_filters():
    region_var.set("All Regions")
    category_var.set("All Categories")
    update_dashboard()


region_box.bind(
    "<<ComboboxSelected>>",
    update_dashboard
)

category_box.bind(
    "<<ComboboxSelected>>",
    update_dashboard
)


# =====================================================
# FOOTER
# =====================================================

footer = tk.Label(
    root,
    text=(
        "RETAIL SALES ANALYTICS  |  "
        "Python • Pandas • Matplotlib • Tkinter"
    ),
    bg=BG,
    fg=MUTED,
    font=("Segoe UI", 9)
)

footer.pack(pady=(0, 8))


# =====================================================
# START DASHBOARD
# =====================================================

update_dashboard()
root.mainloop()