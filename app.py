from dotenv import load_dotenv
load_dotenv()

import os
import streamlit as st
import sqlite3


from langchain_google_genai import ChatGoogleGenerativeAI



gemini_ai_key = os.getenv("gemini_ai_key")



# LLM setup
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=gemini_ai_key,
    temperature=0.2
)

# Generate SQL
def get_sql_query(question, prompt):
    try:
        response = llm.invoke([
            ("system", prompt),
            ("human", question)
        ])

        # ✅ correct extraction
        sql = response.content

        # ✅ clean SQL
        sql = sql.replace("```sql", "").replace("```", "").strip()

        # ✅ ensure valid SQL ends with ;
        if ";" in sql:
            sql = sql.split(";")[0] + ";"

        return sql

    except Exception as e:
        print("Error:", e)
        return None


# Execute SQL
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()

    cur.execute(sql)
    rows = cur.fetchall()

    conn.close()
    return rows


# Prompt
prompt = """
You are a helpful assistant that generates SQL queries.

Database:
Table: companies
Columns:
- id
- name
- employee
- department

IMPORTANT:
- Return ONLY SQL query
- No explanation
- No text

Examples:

User Question: List all companies and their employees
SQL Query: SELECT name, employee FROM companies;

User Question: Show all employees
SQL Query: SELECT employee FROM companies;
"""


# Streamlit UI
st.title("SQL Query Generator (Gemini)")

user_question = st.text_input("Ask a question about the database:")

if st.button("Generate SQL Query"):
    if user_question:
        sql_query = get_sql_query(user_question, prompt)

        if not sql_query:
            st.error("Failed to generate SQL query")
            st.stop()

        st.subheader("Generated SQL Query:")
        st.code(sql_query)

        try:
            results = read_sql_query(sql_query, 'companies.db')

            st.subheader("Query Results:")
            if results:
                for row in results:
                    st.write(row)
            else:
                st.write("No results found.")

        except Exception as e:
            st.error(f"SQL Error: {e}")

    else:
        st.warning("Please enter a question.")