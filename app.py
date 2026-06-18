import streamlit as st
import sqlite3
import plotly.express as px
import os

st.set_page_config(page_title="Retail Sales Dashboard", layout="wide")

if not os.path.exists('data'):
    os.makedirs('data')

if not os.path.exists('data/retail_sales.sqlite'):
    st.info("Creating database...")
    import subprocess
    subprocess.run(["python", "create_db.py"])

conn = sqlite3.connect('data/retail_sales.sqlite')
df = conn.execute("SELECT * FROM sales").fetchall()
conn.close()

columns = ['sales_id', 'product_category', 'region', 'customer_segment', 'month', 'revenue', 'quantity']
data = [dict(zip(columns, row)) for row in df]

st.sidebar.title("Filters")
category = st.sidebar.multiselect("Category", sorted(set(r['product_category'] for r in data)), default=sorted(set(r['product_category'] for r in data)))
region = st.sidebar.multiselect("Region", sorted(set(r['region'] for r in data)), default=sorted(set(r['region'] for r in data)))

filtered = [r for r in data if r['product_category'] in category and r['region'] in region]

st.title("🛒 Retail Sales Dashboard with AI Agent")
st.markdown("### KPIs")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
total_rev = sum(r['revenue'] for r in filtered)
avg_order = total_rev / len(filtered) if filtered else 0
top_cat = max(set(r['product_category'] for r in filtered), key=lambda x: sum(r['revenue'] for r in filtered if r['product_category'] == x))

kpi1.metric("Total Revenue", f"${total_rev:.0f}")
kpi2.metric("Avg Order", f"${avg_order:.2f}")
kpi3.metric("Orders", f"{len(filtered)}")
kpi4.metric("Top Category", top_cat)

st.markdown("### Charts")
c1, c2 = st.columns(2)

with c1:
    cat_rev = {cat: sum(r['revenue'] for r in filtered if r['product_category'] == cat) for cat in set(r['product_category'] for r in filtered)}
    fig1 = px.bar(x=list(cat_rev.keys()), y=list(cat_rev.values()), title="By Category")
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    reg_rev = {reg: sum(r['revenue'] for r in filtered if r['region'] == reg) for reg in set(r['region'] for r in filtered)}
    fig2 = px.pie(values=list(reg_rev.values()), names=list(reg_rev.keys()), title="By Region")
    st.plotly_chart(fig2, use_container_width=True)

month_rev = {m: sum(r['revenue'] for r in filtered if r['month'] == m) for m in set(r['month'] for r in filtered)}
fig3 = px.line(x=list(month_rev.keys()), y=list(month_rev.values()), title="Monthly Trend")
st.plotly_chart(fig3, use_container_width=True)

st.markdown("### AI Agent: Natural Language → SQL")
query = st.text_input("Ask: 'Top category?', 'Avg revenue?'")
if query:
    sql = "SELECT * FROM sales LIMIT 10"
    if 'top' in query.lower() and 'category' in query.lower():
        sql = "SELECT product_category, SUM(revenue) as total FROM sales GROUP BY product_category ORDER BY total DESC LIMIT 5"
    elif 'avg' in query.lower():
        sql = "SELECT AVG(revenue) FROM sales"
    st.code(sql, language='sql')
    conn = sqlite3.connect('data/retail_sales.sqlite')
    result = conn.execute(sql).fetchall()
    conn.close()
    for row in result:
        st.write(row)

if st.button("Export CSV"):
    import csv
    with open('export.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(columns)
        writer.writerows(filtered)
    st.success("Exported!")
