# RetailVision

### Retail Sales Analytics & Business Intelligence Dashboard

RetailVision is a Python-based retail sales analysis dashboard that transforms sales data into meaningful business insights through interactive visualizations and performance indicators.

The project analyzes retail sales across different product categories, regions, and months to help identify sales trends and understand business performance.

## Project Objectives

* Analyze retail sales data using Python.
* Identify high-performing product categories and regions.
* Understand monthly sales trends.
* Visualize important business performance indicators.
* Present analytical results through a graphical dashboard.

## Features

* **Total Sales:** Displays total sales revenue.
* **Total Orders:** Shows the number of unique orders.
* **Units Sold:** Displays the total quantity sold.
* **Total Profit:** Summarizes profit recorded in the dataset.
* **Monthly Sales Trend:** Visualizes changes in sales over time.
* **Category Analysis:** Compares sales across product categories.
* **Regional Analysis:** Identifies high-performing sales regions.
* **Category Sales Distribution:** Displays each category's contribution to total sales.
* **Interactive Filters:** Filter the dashboard by region and product category.
* **Business Insights:** Highlights the top-performing category and region.

## Technologies Used

* Python
* Pandas
* Matplotlib
* Tkinter
* CSV

## Dataset

The project uses retail sales data from a Kaggle Superstore dataset.

The dataset contains information about orders, order dates, product categories, regions, sales, quantities, and profits when available.

The dashboard uses the existing sales values in the dataset rather than calculating revenue from quantity and unit price.

**Note:** Keep the dataset file named `sales_data.csv` in the project folder. If the dataset is obtained from Kaggle, retain the original dataset attribution and follow its licensing terms.

## Project Structure

```text
RetailVision/
├── dashboard.py
├── sales_data.csv
└── README.md
```

## Installation

### Step 1: Install Python

Install Python if it is not already available on your system.

### Step 2: Install Required Libraries

Open a terminal in the project folder and run:

```bash
python -m pip install pandas matplotlib
```

### Step 3: Prepare the Dataset

Place the Kaggle Superstore CSV file in the project folder and rename it to:

```text
sales_data.csv
```

### Step 4: Run the Dashboard

Execute the following command:

```bash
python dashboard.py
```

The dashboard window will open and display sales metrics, charts, and business insights.

## Learning Outcomes

Through this project, I developed practical experience in:

* Loading and cleaning CSV data using Pandas.
* Performing sales analysis and aggregation.
* Creating charts and visualizations using Matplotlib.
* Developing a graphical user interface using Tkinter.
* Using interactive filters to explore data.
* Presenting data-driven business insights.

## Future Enhancements

* Add date-range filters.
* Introduce product-level performance analysis.
* Export filtered reports to CSV or PDF.
* Add more advanced business intelligence metrics.
* Improve dashboard customization and reporting.

## Author

**Kajal Yadav**

MCA Student — Artificial Intelligence and Machine Learning

## Project Purpose

This project was developed as a learning project to practice Python programming, data analysis, data visualization, and dashboard development.
