import sqlite3
import streamlit as st
import requests
import json

# Page configuration
st.set_page_config(
    page_title="Employee Training Hub",
    page_icon="🎓",
    layout="wide"
)

# Custom CSS for professional look
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        borderRadius: 10px;
        color: white;
    }
    .chat-container {
        background: #f0f2f5;
        padding: 1rem;
        borderRadius: 10px;
        min-height: 400px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">🎓 Employee Training Hub</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Product Knowledge & AI Training Assistant</div>', unsafe_allow_html=True)
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
    duration_minutes INTEGER,
    completed BOOLEAN DEFAULT 0
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY,
    name TEXT,
    department TEXT,
    completed_lessons INTEGER DEFAULT 0
)
''')

# Insert sample data if empty
cursor.execute('SELECT COUNT(*) FROM products')
if cursor.fetchone()[0] == 0:
    products = [
        ('Product A', 'Electronics', 299.99, 'High-quality electronic device', 'WiFi, Bluetooth, 4K display'),
        ('Product B', 'Software', 149.99, 'Business management software', 'Cloud-based, AI-powered, Secure'),
        ('Product C', 'Hardware', 499.99, 'Professional workstation', 'Fast processor, Large storage, Gaming-ready'),
    ]
    cursor.executemany('INSERT INTO products (name, category, price, description, features) VALUES (?, ?, ?, ?, ?)', products)
    
    lessons = [
        ('Product Basics', 'Introduction', 'Learn about our product line and categories', 30, 0),
        ('Customer Communication', 'Sales', 'How to effectively communicate with customers', 45, 0),
        ('Technical Support', 'Support', 'Troubleshooting common product issues', 60, 0),
        ('Advanced Features', 'Products', 'Deep dive into product features', 40, 0),
    ]
    cursor.executemany('INSERT INTO lessons (title, category, content, duration_minutes, completed) VALUES (?, ?, ?, ?, ?)', lessons)
    
    employees = [
        ('John Doe', 'Sales', 3),
        ('Jane Smith', 'Support', 4),
        ('Mike Johnson', 'Sales', 2),
    ]
    cursor.executemany('INSERT INTO employees (name, department, completed_lessons) VALUES (?, ?, ?)', employees)
    
    conn.commit()

conn.close()

# Sidebar
st.sidebar.title("📑 Navigation")
page = st.sidebar.radio("Go to", ["💬 AI Training Assistant", "📦 Product Database", "📚 Lesson Management", "👥 Employee Progress"])

st.divider()

# AI Training Assistant Page
if page == "💬 AI Training Assistant":
    st.markdown('<div class="main-header">💬 AI Training Assistant</div>', unsafe_allow_html=True)
    st.markdown("Ask questions about products, lessons, or get training guidance!")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask about products, lessons, or training..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.write(prompt)
        
        with st.chat_message("assistant"):
            # Simple AI response (you can replace with real AI API)
            response = generate_ai_response(prompt)
            st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

def generate_ai_response(prompt):
    """Simple AI response - replace with real API for production"""
    prompt_lower = prompt.lower()
    
    if 'product' in prompt_lower:
        conn = sqlite3.connect('training_data.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name, category, price, description FROM products")
        products = cursor.fetchall()
        conn.close()
        
        response = "Here are our products:
"
        for p in products:
            response += f"
* *{p[0]}* ({p[1]}) - ${p[2]}
  {p[3]}"
        return response
    
    elif 'lesson' in prompt_lower or 'training' in prompt_lower:
        conn = sqlite3.connect('training_data.db')
        cursor = conn.cursor()
        cursor.execute("SELECT title, category, duration_minutes FROM lessons")
        lessons = cursor.fetchall()
        conn.close()
        
        response = "Available training lessons:
"
        for l in lessons:
            response += f"
* *{l[0]}* ({l[1]}) - {l[2]} minutes"
        return response
    
    elif 'employee' in prompt_lower or 'progress' in prompt_lower:
        conn = sqlite3.connect('training_data.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name, department, completed_lessons FROM employees")
        employees = cursor.fetchall()
        conn.close()
        
        response = "Employee progress:
"
        for e in employees:
            response += f"
* *{e[0]}* ({e[1]}) - {e[2]} lessons completed"
        return response
    
    else:
        return "I can help you with product information, training lessons, and employee progress. Ask me about products, lessons, or employees!"

# Product Database Page
elif page == "📦 Product Database":
    st.markdown('<div class="main-header">📦 Product Database</div>', unsafe_allow_html=True)
    
    conn = sqlite3.connect('training_data.db')
    df = conn.execute("SELECT name, category, price, description, features FROM products").fetchall()
    conn.close()
    
    # Metrics
    total_products = len(df)
    total_value = sum(row[2] for row in df)
    categories = len(set(row[1] for row in df))
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Products", total_products)
    col2.metric("Total Inventory Value", f"${total_value:.2f}")
    col3.metric("Product Categories", categories)
    
    st.divider()
    
    # Search
    search_term = st.text_input("🔍 Search products...", placeholder="Search by name or category")
    
    if search_term:
        df_filtered = [row for row in df if search_term.lower() in row[0].lower() or search_term.lower() in row[1].lower()]
    else:
        df_filtered = df
    
    # Display products
    for row in df_filtered:
        with st.card():
            st.subheader(row[0])
            st.caption(f"Category: {row[1]}")
            st.markdown(f"*Price:* ${row[2]:.2f}")
            st.markdown(f"*Description:* {row[3]}")
            st.markdown(f"*Features:* {row[4]}")
            st.divider()

# Lesson Management Page
elif page == "📚 Lesson Management":
    st.markdown('<div class="main-header">📚 Lesson Management</div>', unsafe_allow_html=True)
    
    conn = sqlite3.connect('training_data.db')
    lessons = conn.execute("SELECT title, category, content, duration_minutes, completed FROM lessons").fetchall()
    conn.close()
    
    # Metrics
    total_lessons = len(lessons)
    completed = sum(1 for l in lessons if l[4] == 1)
    avg_duration = sum(l[3] for l in lessons) / total_lessons
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Lessons", total_lessons)
    col2.metric("Completed", completed)
    col3.metric("Avg Duration", f"{avg_duration:.0f} min")
    
    st.divider()
    
    # Display lessons
    for lesson in lessons:
        with st.expander(f"📖 {lesson[0]} ({lesson[1]}) - {lesson[3]} min"):
            st.markdown(lesson[2])
            status = "✅ Completed" if lesson[4] == 1 else "⏳ Not Started"
            st.caption(status)

# Employee Progress Page
elif page == "👥 Employee Progress":
    st.markdown('<div class="main-header">👥 Employee Progress</div>', unsafe_allow_html=True)
    
    conn = sqlite3.connect('training_data.db')
    employees = conn.execute("SELECT name, department, completed_lessons FROM employees").fetchall()
    conn.close()
    
    # Metrics
    total_employees = len(employees)
    total_completed = sum(e[2] for e in employees)
    avg_completed = total_completed / total_employees
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Employees", total_employees)
    col2.metric("Total Lessons Completed", total_completed)
    col3.metric("Avg per Employee", f"{avg_completed:.1f}")
    
    st.divider()
    
    # Display employees
    for emp in employees:
        st.write(f"👤 *{emp[0]}* ({emp[1]}) - {emp[2]} lessons completed")
