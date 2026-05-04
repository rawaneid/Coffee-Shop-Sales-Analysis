# ☕ Coffee Shop Sales Analytics Dashboard

An interactive sales analytics dashboard built with **Streamlit** and **Plotly**, exploring transaction data from a 3-location coffee shop chain across January–June 2023.

---

## 📊 Project Overview

This project analyzes **149,116 transactions** totaling **$698,812** in revenue across three New York City locations — Astoria, Hell's Kitchen, and Lower Manhattan. The dashboard surfaces key business insights around revenue trends, peak hours, product performance, and store comparisons through an elegant, coffee-themed UI.

---

## 🗂️ Project Structure

```
├── Home.py                          # Main Streamlit app (all pages)
├── Coffee_shop_sales.csv            # Raw transaction data
├── Coffee_shop_sales_cleaned.csv    # Cleaned dataset (used by the app)
├── coffee_shop.ipynb                # EDA & data cleaning notebook
├── config.toml                      # Streamlit theme configuration
└── README.md
```

---

## 🧭 Dashboard Pages

| Page | Description |
|---|---|
| 🏠 **Overview** | High-level KPIs, revenue by store, monthly trends, and business insights |
| 📅 **Time Trends** | Revenue by hour, day of week, time of day, and a Day × Hour heatmap |
| ☕ **Products** | Top products by revenue, category mix, order size distribution, and store comparisons |
| 📋 **About Dataset** | Column reference guide and a live preview of the cleaned data |

---

## 📁 Dataset

### Key Columns

| Column | Description |
|---|---|
| `transaction_id` | Unique transaction identifier |
| `transaction_date` | Full timestamp of the transaction |
| `store_location` | Astoria · Hell's Kitchen · Lower Manhattan |
| `transaction_qty` | Number of items in the order |
| `unit_price` | Price per item |
| `Total_Bill` | Transaction total (qty × unit price) |
| `product_category` | Coffee, Tea, Bakery, Chocolate, etc. |
| `product_type` | Specific product sub-type (e.g. Barista Espresso) |
| `Size` | Small · Regular · Large · Not Defined |
| `Hour` | Hour of transaction (6 AM – 8 PM) |
| `Day Name` | Day of the week |
| `Month Name` | Month name |
| `Day_time` | Morning · Afternoon · Evening · Night |
| `Day_Type` | Weekday or Weekend |

---

## 🔍 Key Insights

- 📈 **Revenue grew 103.8%** from January to June 2023
- ⏰ **Peak hours are 8–10 AM**, with mornings driving the majority of all sales
- 📅 **Monday is the highest-revenue day**; Saturday is the slowest
- ☕ **Barista Espresso** is the top-earning product type
- 📏 **Large orders earn ~59% more** than Small — upselling has a measurable impact
- 🏪 All three stores share a **consistent product mix**, indicating a scalable business model

---

## 🚀 Getting Started

### Prerequisites

```bash
pip install streamlit pandas plotly
```

### Run the App

```bash
streamlit run Home.py
```

Make sure `Coffee_shop_sales_cleaned.csv` is in the same directory as `Home.py`.

---

## 📓 Notebook

`coffee_shop.ipynb` contains the exploratory data analysis (EDA) and data cleaning steps used to transform the raw CSV into the cleaned dataset powering the dashboard.
