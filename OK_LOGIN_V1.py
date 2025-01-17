import streamlit as st
import pandas as pd
import oracledb
from sqlalchemy import create_engine

st.title("Welcome to One-Key Audits")

orgid = st.text_input("Org ID")
username = st.text_input("OCE Admin UserName")
password = st.text_input("OCE Admin Password", type="password")

env = ["Sandbox","Production"]



st.title("One Key Audit Results")
st.selectbox("Select the environment",env)

dsn = oracledb.makedsn("10.160.36.20", "1521", service_name="ATIGER1P.CEGEDIM.COM")

def create_connection():
    """Create a connection to the Oracle database."""
    try:
        conn = oracledb.connect(
            user="gsops",
            password="2JpGL?cm",
            dsn=dsn
        )
        return conn
    except oracledb.DatabaseError as e:
        st.error(f"Error connecting to database: {e}")
        return None

def query_db(conn, query):
    """Query the database and return the results as a DataFrame."""
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        df = pd.DataFrame(rows, columns=columns)
        cursor.close()
        return df
    except oracledb.DatabaseError as e:
        st.error(f"Error running query: {e}")
        return pd.DataFrame()

# Streamlit app
st.title("Oracle Database Connection Example")

# Sample query
query = "SELECT * FROM ONEKEY_AUDIT_MASTER"

# Create connection
conn = create_connection()

if conn:
    st.write("Connected to the database successfully!")

    # Query the database
    df = query_db(conn, query)

    # Display results
    if not df.empty:
        st.write("Query Results:")
        st.dataframe(df)
    else:
        st.error("No data retrieved from the database.")

    # Close the connection
    conn.close()
else:
    st.error("Failed to connect to the database.")

if st.button("Download Excel"):
    df.to_excel("abc.xlsx", index=False)
    st.write("Results exported to abc.xlsx")
else:
    st.write("No records found.")
st.button("Run Audit")
