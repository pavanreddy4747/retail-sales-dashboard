import sqlite3
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Employee Training Hub",
    page_icon="🎓",
    layout="wide"
)

# Header
st.title("🎓 Employee Training Hub")
st.subheader("Product Knowledge & AI Training Assistant")
st.divider()

# Create database
conn = sqlite3.connect('training_data.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY,
    name TEXT,
    category TEXT,
    price REAL,
    description TEXT,
    features TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS lessons (
    id INTEGER PRIMARY KEY,
    title TEXT,
    category TEXT,
    content TEXT,
    duration_minutes INTEGER
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY,
    name TEXT,
    department TEXT,
    completed_lessons INTEGER
)
''')

# Insert sample data
cursor.execute('SELECT COUNT(*) FROM products')
if cursor.fetchone()[0] == 0:
    products = [
        ('Product A', 'Electronics', 299.99, 'High-quality electronic device', 'WiFi, Bluetooth, 4K'),
        ('Product B', 'Software', 149.99, 'Business management software', 'Cloud-based, AI-powered'),
        ('Product C', 'Hardware', 499.99, 'Professional workstation', 'Fast processor, Large storage'),
    ]
    cursor.executemany('INSERT INTO products (name, category, price, description, features) VALUES (?, ?, ?, ?, ?)', products)
    
    lessons = [
        ('Product Basics', 'Introduction', 'Learn about products', 30),
        ('Customer Communication', 'Sales', 'How to communicate with customers', 45),
        ('Technical Support', 'Support', 'Troubleshooting issues', 60),
    ]
    cursor.executemany('INSERT INTO lessons (title, category, content, duration_minutes) VALUES (?, ?, ?, ?)', lessons)
    
    employees = [
        ('John Doe', 'Sales', 3),
        ('Jane Smith', 'Support', 4),
    ]
    cursor.executemany('INSERT INTO employees (name, department, completed_lessons) VALUES (?, ?, ?)', employees)
    
    conn.commit()

conn.close()

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["AI Assistant", "Products", "Lessons", "Employees"])

st.divider()

# AI Assistant
if page == "AI Assistant":
    st.title("💬 AI Training Assistant")
    st.write("Ask questions about products, lessons, or training!")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    if prompt := st.chat_input("Ask something..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        
        with st.chat_message("assistant"):
            response = get_ai_response(prompt)
            st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

def get_ai_response(prompt):
    prompt_lower = prompt.lower()
    
    if 'product' in prompt_lower:
        conn = sqlite3.connect('training_data.db')
        products = conn.execute("SELECT name, category, price FROM products").fetchall()
        conn.close()
        response = "Our products:
"
        for p in products:
            response += f"
* {p[0]} ({p[1]}) - ${p[2]}"
        return response
    
    elif 'lesson' in prompt_lower:
        conn = sqlite3.connect('training_data.db')
        lessons = conn.execute("SELECT title, category FROM lessons").fetchall()
        conn.close()
        response = "Available lessons:
"
        for l in lessons:
            response += f"
* {l[0]} ({l[1]})"
        return response
    
    else:
        return "I can help with products, lessons, and employees. Ask about any of these!"

# Products
elif page == "Products":
    st.title("📦 Product Database")
    
    conn = sqlite3.connect('training_data.db')
    products = conn.execute("SELECT name, category, price, description, features FROM products").fetchall()
    conn.close()
    
    st.metric("Total Products", len(products))
    st.divider()
    
    for p in products:
        st.subheader(p[0])
        st.write(f"*Category:* {p[1]}")
        st.write(f"*Price:* ${p[2]}")
        st.write(f"*Description:* {p[3]}")
        st.write(f"*Features:* {p[4]}")
        st.divider()

# Lessons
elif page == "Lessons":
    st.title("📚 Lesson Management")
    
    conn = sqlite3.connect('training_data.db')
    lessons = conn.execute("SELECT title, category, content, duration_minutes FROM lessons").fetchall()
    conn.close()
    
    st.metric("Total Lessons", len(lessons))
    st.divider()
    
    for l in lessons:
        with st.expander(f"{l[0]} ({l[1]}) - {l[3]} min"):
            st.write(l[2])

# Employees
elif page == "Employees":
    st.title("👥 Employee Progress")
    
    conn = sqlite3.connect('training_data.db')
    employees = conn.execute("SELECT name, department, completed_lessons FROM employees").fetchall()
    conn.close()
    
    st.metric("Total Employees", len(employees))
    st.divider()
    
    for e in employees:
        st.write(f"*{e[0]}* ({e[1]}) - {e[2]} lessons completed")
