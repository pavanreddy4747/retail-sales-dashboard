import sqlite3
import streamlit as st

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
    ]
    cursor.executemany('''
    INSERT INTO sales (date, product, quantity, price)
    VALUES (?, ?, ?, ?)
    ''', sample_data)
    conn.commit()

conn.close()

# Now read the data
conn = sqlite3.connect('sales_data.db')
df = conn.execute("SELECT * FROM sales").fetchall()
conn.close()

# Display in Streamlit
st.title("Retail Sales Dashboard")
st.subheader("Sales Data")
st.write(df)
