import streamlit as st
from sqlalchemy import create_engine, text

# Read from Streamlit secrets
DB_USER = st.secrets["user"]
DB_PASS = st.secrets["password"]
DB_HOST = st.secrets["host"]
DB_PORT = st.secrets["port"]
DB_NAME = st.secrets["dbname"]

# Build connection URL
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

def insert_log(action, answer):
    with engine.begin() as conn:
        conn.execute(
            text("INSERT INTO logs (action, answer) VALUES (:a, :b)"),
            {"a": action, "b": answer}
        )

def fetch_logs():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM logs")).fetchall()
        return result

