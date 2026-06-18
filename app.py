import sqlite3
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Retail Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

# Create database and table if they don't exist
conn = sqlite3.connect('sales_data.db')
cursor = conn.cursor()

# Create table
cursor.execute('''
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY,
    date TEXT,
    product TEXT,
    quantity INTEGER,
    price REAL
)
''')

# Insert sample data if table is empty
cursor.execute('SELECT COUNT(*) FROM sales')
if cursor.fetchone()[0] == 0:
    sample_data = [
        ('2024-01-01', 'Product A', 10, 25.5),
        ('2024-01-02', 'Product B', 5, 30.0),
        ('2024-01-03', 'Product A', 8, 25.5),
        ('2024-01-04', 'Product C', 12, 15.0),
        ('2024-01-05', 'Product B', 7, 30.0),
        ('2024-01-06', 'Product A', 15, 25.5),
        ('2024-01-07', 'Product C', 20, 15.0),
        ('2024-01-08', 'Product B', 12, 30.0),
        ('2024-01-09', 'Product A', 18, 25.5),
        ('2024-01-10', 'Product C', 25, 15.0),
    ]
    cursor.executemany('''
    INSERT INTO sales (date, product, quantity, price)
    VALUES (?, ?, ?, ?)
    ''', sample_data)
    conn.commit()

conn.close()

# Read the data
conn = sqlite3.connect('sales_data.db')
df = conn.execute("SELECT * FROM sales").fetchall()
conn.close()

# Convert to list of dicts for easier handling
sales_data = []
for row in df:
    sales_data.append({
        'id': row[1],
        'date': row[2],
        'product': row[3],
        'quantity': row[4],
        'price': row[5],
        'total': row[4] * row[5]
    })

# Dashboard Header
st.title("📊 Retail Sales Dashboard")
st.markdown("### Real-time Sales Analytics & Performance Metrics")
st.divider()

# Summary Metrics
total_sales = sum(item['total'] for item in sales_data)
total_quantity = sum(item['quantity'] for item in sales_data)
total_transactions = len(sales_data)
avg_transaction = total_sales / total_transactions if total_transactions > 0 else 0

st.markdown("### 📈 Key Metrics")
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Sales Revenue", f"${total_sales:.2f}")
col2.metric("Total Quantity Sold", total_quantity)
col3.metric("Total Transactions", total_transactions)
col4.metric("Avg Transaction Value", f"${avg_transaction:.2f}")

st.divider()

# Charts
st.markdown("### 📊 Sales Analytics")

# Product Sales Chart
col1, col2 = st.columns(2)

with col1:
    st.subheader("Sales by Product")
    product_sales = {}
    for item in sales_data:
        product_sales[item['product']] = product_sales.get(item['product'], 0) + item['total']
    
    fig_pie = px.pie(
        values=list(product_sales.values()),
        names=list(product_sales.keys()),
        title='Revenue Distribution',
        color_discrete_sequence=px.colors.sequential.Agsunset
    )
    fig_pie.update_traces(textposition='auto', textinfo='percent+label+value')
    st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    st.subheader("Quantity Sold by Product")
    fig_bar = px.bar(
        x=list(product_sales.keys()),
        y=[product_sales[p] for p in product_sales.keys()],
        title='Revenue by Product',
        color=list(product_sales.keys()),
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    fig_bar.update_layout(xaxis_title="Product", yaxis_title="Revenue ($)")
    st.plotly_chart(fig_bar, use_container_width=True)

# Sales Trend Chart
st.subheader("Sales Trend Over Time")
dates = [item['date'] for item in sales_data]
totals = [item['total'] for item in sales_data]

fig_line = px.line(
    x=dates,
    y=totals,
    title='Daily Sales Trend',
    markers=True
)
fig_line.update_traces(line=dict(color='#1f77b4', width=3))
fig_line.update_layout(xaxis_title="Date", yaxis_title="Revenue ($)")
st.plotly_chart(fig_line, use_container_width=True)

st.divider()

# Data Table
st.markdown("### 📋 Detailed Sales Data")
st.dataframe(
    sales_data,
    use_container_width=True,
    hide_index=True
)

# Footer
st.divider()
st.markdown(
    """
    <div style='text-align: center; color: grey;'>
        <p>🚀 Built with Streamlit | Data-driven Retail Analytics</p>
        <p>Check out my GitHub for more projects!</p>
    </div>
    ",
    unsafe_allow_html=True
)
