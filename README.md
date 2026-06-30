# 📊 Retail Sales Exploratory Data Analysis

An end-to-end Exploratory Data Analysis (EDA) project on a retail sales dataset, built with Python, pandas, and seaborn/matplotlib. The project covers data cleaning, descriptive statistics, time series trends, customer & product segmentation, correlation analysis, and visual reporting — concluding with data-driven business recommendations.

## 🔍 Overview

This script ingests a raw retail transactions dataset and walks through a complete analytical workflow:

1. **Data Loading & Cleaning** – parses dates, extracts year/month/quarter, handles missing values and duplicates.
2. **Descriptive Statistics** – summary stats (mean, median, mode) for age, quantity, price, and total amount, plus overall revenue metrics.
3. **Time Series Analysis** – monthly revenue trend with a 3-month rolling average, and quarterly revenue breakdown.
4. **Customer & Product Analysis**
   - Revenue split by gender
   - Customer age distribution and revenue by age group
   - Revenue & order count by product category
   - Category × gender revenue heatmap
   - Monthly revenue trend per product category
   - Price vs. quantity scatter analysis
   - Correlation matrix of numeric features
5. **Top Customers** – identifies and visualizes the top 10 customers by total revenue.
6. **Recommendations** – auto-generated business insights based on the analysis (top category, top age segment, peak sales month, etc.).

## 🛠️ Tech Stack

- **Python 3**
- **pandas** & **NumPy** – data manipulation
- **matplotlib** & **seaborn** – visualization
- **pathlib** – output management

## 📂 Output

Running the script generates 10 charts saved to the `eda_outputs/` folder, including:

| File | Description |
|---|---|
| `01_monthly_revenue.png` | Monthly revenue with rolling average |
| `02_quarterly_revenue.png` | Quarterly revenue breakdown |
| `03_gender_age.png` | Revenue by gender & age distribution |
| `04_revenue_by_age_group.png` | Revenue by age group |
| `05_product_category.png` | Revenue & orders by product category |
| `06_heatmap_category_gender.png` | Category × gender revenue heatmap |
| `07_category_monthly_trend.png` | Monthly trend per category |
| `08_price_vs_quantity.png` | Price vs. quantity scatter |
| `09_correlation_matrix.png` | Correlation matrix of numeric features |
| `10_top_customers.png` | Top 10 customers by revenue |

## 🚀 Getting Started

### Prerequisites
```bash
pip install pandas numpy matplotlib seaborn
```

### Run
1. Place your dataset as `retail_sales_dataset.csv` in the project directory.
2. Run the script:
```bash
python retail_sales_eda.py
```
3. Check the `eda_outputs/` folder for generated charts and the console for printed statistics and recommendations.

## 📈 Key Insights

The analysis automatically surfaces:
- The top-performing product category by revenue
- The most valuable customer age segment
- The peak sales month
- Pricing and bundling opportunities based on price–quantity patterns
- Customer retention opportunities via top-customer identification

**Sania Aftab**

## 📄 License

Feel free to use and adapt this project for your own learning or portfolio.
