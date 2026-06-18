import sqlite3
import streamlit as st

st.title("📊 Retail Sales Dashboard")
st.markdown("### Sales Analytics")

# Create database
conn = sqlite3.connect('sales_data.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY,
    date TEXT,
    product TEXT,
    quantity INTEGER,
    price REAL
)
''')

cursor.execute('SELECT COUNT(*) FROM sales')
if cursor.fetchone()[0] == 0:
    sample_data = [
        ('2024-01-01', 'Product A', 10, 25.5),
        ('2024-01-02', 'Product B', 5, 30.0),
        ('2024-01-03', 'Product A', 8, 25.5),
        ('2024-01-04', 'Product C', 12, 15.0),
        ('2024-01-05', 'Product B', 7, 30.0),
    ]
    cursor.executemany('INSERT INTO sales (date, product, quantity, price) VALUES (?, ?, ?, ?)', sample_data)
    conn.commit()

conn.close()

# Read data
conn = sqlite3.connect('sales_data.db')
rows = conn.execute("SELECT * FROM sales").fetchall()
conn.close()

# Display
st.markdown("### 📋 Sales Data")
for row in rows:
    id_val = row[0]
    date_val = row[1]
    product_val = row[2]
    quantity_val = row[3]
    price_val = row[4]
    total_val = quantity_val * price_val
    st.write(f"*ID:* {id_val} | *Date:* {date_val} | *Product:* {product_val} | *Qty:* {quantity_val} | *Price:* ${price_val} | *Total:* ${total_val:.2f}")

# Metrics
total_sales = sum(row[3] * row[4] for row in rows)
total_qty = sum(row[3] for row in rows)

st.divider()
col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"${total_sales:.2f}")
col2.metric("Total Quantity", total_qty)
col3.metric("Transactions", len(rows))

st.caption("Built with Streamlit")
