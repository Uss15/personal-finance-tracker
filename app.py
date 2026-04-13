import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os

# Page configuration
st.set_page_config(page_title="Personal Finance Tracker", page_icon="💰", layout="wide")

# Custom CSS for a cleaner look
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #007bff;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# Title and Description
st.title("💰 Personal Finance Tracker")
st.markdown("Track your expenses, visualize your spending habits, and manage your budget effectively.")

# Initialize or load data
DATA_FILE = "expenses.csv"

def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=["Date", "Category", "Description", "Amount"])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# Sidebar for adding new expenses
st.sidebar.header("Add New Expense")
with st.sidebar.form("expense_form", clear_on_submit=True):
    date = st.date_input("Date", datetime.now())
    category = st.selectbox("Category", ["Food", "Transport", "Rent", "Entertainment", "Shopping", "Utilities", "Health", "Others"])
    description = st.text_input("Description")
    amount = st.number_input("Amount ($)", min_value=0.0, step=0.01)
    submit = st.form_submit_button("Add Expense")

    if submit:
        if amount > 0:
            new_data = pd.DataFrame([[date, category, description, amount]], columns=["Date", "Category", "Description", "Amount"])
            df = load_data()
            df = pd.concat([df, new_data], ignore_index=True)
            save_data(df)
            st.sidebar.success("Expense added successfully!")
        else:
            st.sidebar.error("Please enter a valid amount.")

# Main Dashboard
df = load_data()

if not df.empty:
    # Summary Metrics
    col1, col2, col3 = st.columns(3)
    total_spent = df["Amount"].sum()
    avg_spent = df["Amount"].mean()
    num_transactions = len(df)

    col1.metric("Total Spent", f"${total_spent:,.2f}")
    col2.metric("Average Transaction", f"${avg_spent:,.2f}")
    col3.metric("Total Transactions", num_transactions)

    st.divider()

    # Visualizations
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Spending by Category")
        fig_pie = px.pie(df, values='Amount', names='Category', hole=0.4, 
                         color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_right:
        st.subheader("Spending Over Time")
        df['Date'] = pd.to_datetime(df['Date'])
        df_time = df.groupby('Date')['Amount'].sum().reset_index()
        fig_line = px.line(df_time, x='Date', y='Amount', markers=True)
        st.plotly_chart(fig_line, use_container_width=True)

    # Recent Transactions Table
    st.subheader("Recent Transactions")
    st.dataframe(df.sort_values(by="Date", ascending=False), use_container_width=True)

    # Clear Data Option
    if st.button("Clear All Data"):
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)
            st.rerun()
else:
    st.info("No expenses recorded yet. Use the sidebar to add your first expense!")

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit and Plotly")
