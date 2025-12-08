import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Streamlit page config
st.set_page_config(layout="wide", page_title="Blinkit Dashboard")

# Load data
data = pd.read_csv(r"G:\sayed\Career\data science epsilon ai\mid project final\blinkit_data.csv")
st.title("📊 Blinkit Analysis Dashboard")

# Sidebar Filters
st.sidebar.header("Filters")

columns = ['Item Fat Content','Item Identifier','Item Type','Outlet Establishment Year','Outlet Identifier',
           'Outlet Location Type','Outlet Size','Outlet Type','Item Visibility','Item Weight','Sales','Rating']

# Dynamic sidebar filters
def add_sidebar_filter(col):
    unique_vals = data[col].dropna().unique()
    return st.sidebar.multiselect(f"Filter by {col}", unique_vals, default=list(unique_vals))

filters = {}
for col in columns:
    filters[col] = add_sidebar_filter(col)

# Apply filters
filtered_df = data.copy()
for col, vals in filters.items():
    if len(vals) > 0:
        filtered_df = filtered_df[filtered_df[col].isin(vals)]

st.subheader("1️⃣ Total Sales by Fat Content")
sales_by_fat = filtered_df.groupby('Item Fat Content')['Sales'].sum()
fig1, ax1 = plt.subplots()
ax1.pie(sales_by_fat, labels=sales_by_fat.index, autopct='%.0f%%', startangle=90)
ax1.set_title('Sales by Fat Content')
st.pyplot(fig1)


st.subheader("2️⃣ Total Sales by Item Type")
sales_by_type = filtered_df.groupby('Item Type')['Sales'].sum().sort_values(ascending=False)
fig2, ax2 = plt.subplots(figsize=(10,6))
bars = ax2.bar(sales_by_type.index, sales_by_type.values)
ax2.set_xticklabels(sales_by_type.index, rotation=90)
ax2.set_xlabel('Item Type')
ax2.set_ylabel('Total Sales')
ax2.set_title('Total Sales by Item Type')
for bar in bars:
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height(), f'{bar.get_height():,.0f}', ha='center', va='bottom', fontsize=7)
st.pyplot(fig2)


st.subheader("3️⃣ Fat Content Contribution by Outlet Location Type")
grouped = filtered_df.groupby(['Outlet Location Type','Item Fat Content'])['Sales'].sum().unstack()
if 'Regular' in grouped.columns and 'Low Fat' in grouped.columns:
    grouped = grouped[['Regular','Low Fat']]
fig3, ax3 = plt.subplots(figsize=(8,5))
grouped.plot(kind='bar', ax=ax3)
ax3.set_title('Outlet Tier by Item Fat Content')
ax3.set_xlabel('Outlet Location Tier')
ax3.set_ylabel('Total Sales')
ax3.legend(title='Item Fat Content')
st.pyplot(fig3)


st.subheader("4️⃣ Total Sales by Outlet Establishment Year")
sales_by_year = filtered_df.groupby('Outlet Establishment Year')['Sales'].sum().sort_index()
fig4, ax4 = plt.subplots(figsize=(9,5))
ax4.plot(sales_by_year.index, sales_by_year.values, marker='o', linestyle='-')
ax4.set_xlabel('Outlet Establishment Year')
ax4.set_ylabel('Total Sales')
ax4.set_title('Outlet Establishment Sales Trend')
for x, y in zip(sales_by_year.index, sales_by_year.values):
    ax4.text(x, y, f'{y:,.0f}', ha='center', va='bottom', fontsize=8)
st.pyplot(fig4)


st.subheader("5️⃣ Total Sales by Outlet Size")
sales_by_size = filtered_df.groupby('Outlet Size')['Sales'].sum()
fig5, ax5 = plt.subplots(figsize=(5,5))
ax5.pie(sales_by_size, labels=sales_by_size.index, autopct='%1.1f%%', startangle=90)
ax5.set_title('Sales by Outlet Size')
st.pyplot(fig5)


st.subheader("6️⃣ Total Sales by Outlet Location Type")
sales_by_location = filtered_df.groupby('Outlet Location Type')['Sales'].sum().reset_index()
sales_by_location = sales_by_location.sort_values('Sales', ascending=False)
fig6, ax6 = plt.subplots(figsize=(8,5))
sns.barplot(x='Sales', y='Outlet Location Type', data=sales_by_location, ax=ax6)
ax6.set_title('Total Sales by Outlet Location Type')
ax6.set_xlabel('Sales')
ax6.set_ylabel('Outlet Location Type')
st.pyplot(fig6)
