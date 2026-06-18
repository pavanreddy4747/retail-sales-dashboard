import sqlite3
import streamlit as st

st.set_page_config(page_title="Training Hub", page_icon="🎓", layout="wide")

st.title("🎓 Employee Training Hub")
st.subheader("Product Knowledge & AI Assistant")
st.divider()

# Create database
conn = sqlite3.connect('training_data.db')
cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, name TEXT, category TEXT, price REAL, description TEXT, features TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS lessons (id INTEGER PRIMARY KEY, title TEXT, category TEXT, content TEXT, duration_minutes INTEGER)")
cursor.execute("CREATE TABLE IF NOT EXISTS employees (id INTEGER PRIMARY KEY, name TEXT, department TEXT, completed_lessons INTEGER)")

cursor.execute('SELECT COUNT(*) FROM products')
if cursor.fetchone()[0] == 0:
    cursor.executemany("INSERT INTO products (name, category, price, description, features) VALUES (?, ?, ?, ?, ?)", [
        ('Product A', 'Electronics', 299.99, 'High-quality device', 'WiFi, Bluetooth'),
        ('Product B', 'Software', 149.99, 'Business software', 'Cloud-based'),
    ])
    cursor.executemany("INSERT INTO lessons (title, category, content, duration_minutes) VALUES (?, ?, ?, ?)", [
        ('Product Basics', 'Intro', 'Learn products', 30),
        ('Customer Service', 'Sales', 'Communicate well', 45),
    ])
    cursor.executemany("INSERT INTO employees (name, department, completed_lessons) VALUES (?, ?, ?)", [
        ('John', 'Sales', 3),
        ('Jane', 'Support', 4),
    ])
    conn.commit()

conn.close()

# Sidebar
st.sidebar.title("Menu")
page = st.sidebar.radio("Page", ["AI Chat", "Products", "Lessons", "Employees"])
st.divider()

if page == "AI Chat":
    st.title("💬 AI Assistant")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for msg in st.session_state.messages:
        st.write(f"*{msg['role']}:* {msg['content']}")
        st.write("---")
    
    prompt = st.chat_input("Ask about products or lessons...")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.write(f"*user:* {prompt}")
        st.write("---")
        
        response = ai_reply(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.write(f"*assistant:* {response}")
        st.write("---")

def ai_reply(text):
    if 'product' in text.lower():
        conn = sqlite3.connect('training_data.db')
        data = conn.execute("SELECT name, price FROM products").fetchall()
        conn.close()
        return "Products: " + ", ".join([f"{d[0]} (${d[1]})" for d in data])
    elif 'lesson' in text.lower():
        conn = sqlite3.connect('training_data.db')
        data = conn.execute("SELECT title FROM lessons").fetchall()
        conn.close()
        return "Lessons: " + ", ".join([d[0] for d in data])
    else:
        return "Ask about products or lessons!"

elif page == "Products":
    st.title("📦 Products")
    conn = sqlite3.connect('training_data.db')
    data = conn.execute("SELECT name, category, price, description FROM products").fetchall()
    conn.close()
    for d in data:
        st.subheader(d[0])
        st.write(f"Category: {d[1]}")
        st.write(f"Price: ${d[2]}")
        st.write(f"Description: {d[3]}")
        st.divider()

elif page == "Lessons":
    st.title("📚 Lessons")
    conn = sqlite3.connect('training_data.db')
    data = conn.execute("SELECT title, category, duration_minutes FROM lessons").fetchall()
    conn.close()
    for d in data:
        st.write(f"*{d[0]}* ({d[1]}) - {d[2]} min")

elif page == "Employees":
    st.title("👥 Employees")
    conn = sqlite3.connect('training_data.db')
    data = conn.execute("SELECT name, department, completed_lessons FROM employees").fetchall()
    conn.close()
    for d in data:
        st.write(f"*{d[0]}* ({d[1]}) - {d[2]} lessons")
