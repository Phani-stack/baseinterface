import mysql.connector
import os
import re
from dotenv import load_dotenv
from model.state import State
from llm.llm import choose_llm

load_dotenv()

config = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "port": int(os.getenv("DB_PORT", "4000")),
    "database": os.getenv("DB_NAME")
}

def clean_sql(query):
    query = re.sub(r'```sql\s*', '', query, flags=re.IGNORECASE)
    query = re.sub(r'```\s*', '', query)
    query = re.sub(r'^(here\'s the query|the query is|sql query):\s*', '', query, flags=re.IGNORECASE)
    query = query.strip().rstrip(';') + ';'
    return query

def tune_user_query(state):
    try:
        model = choose_llm("low")
        prompt = f"""Make this query clear and specific for database search:
{state.original_user_query}

Output only the refined query:"""

        response = model.invoke(prompt)
        state.tuned_user_query = response.content.strip()
    except Exception as e:
        state.error = f"Error: {str(e)}"
        state.tuned_user_query = state.original_user_query

    return state

def database_context(state):
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor(dictionary=True)

        context = {}

        cursor.execute("SELECT DATABASE() AS database_name")
        context["database"] = cursor.fetchone()["database_name"]

        cursor.execute("SHOW TABLES")
        tables = [row[f"Tables_in_{config['database']}"] for row in cursor.fetchall()]

        for table in tables:
            cursor.execute(f"DESCRIBE `{table}`")
            columns = cursor.fetchall()

            cursor.execute(f"SELECT COUNT(*) AS total_rows FROM `{table}`")
            count = cursor.fetchone()["total_rows"]

            cursor.execute(f"SELECT * FROM `{table}` LIMIT 3")
            rows = cursor.fetchall()

            context[table] = {
                "columns": [{"name": col["Field"], "type": col["Type"], "key": col["Key"]} for col in columns],
                "total_rows": count,
                "sample_rows": rows
            }

        state.database_context = context
        cursor.close()
        conn.close()

    except Exception as e:
        state.error = f"Database error: {str(e)}"
        state.database_context = {}

    return state

def sql_query(state):
    try:
        if state.error:
            return state

        model = choose_llm("high")

        context_text = f"Database: {state.database_context.get('database', 'unknown')}\n\n"
        for table_name, table_info in state.database_context.items():
            if table_name == "database":
                continue
            context_text += f"\nTable: {table_name} ({table_info['total_rows']} rows)\n"
            for col in table_info['columns']:
                context_text += f"  - {col['name']} ({col['type']})\n"
        prompt = f"""Generate SQL query:
                    DATABASE: {context_text}
                    USER QUERY: {state.tuned_user_query}
                    Rules:
                    - Use SELECT only
                    - If no limit mentioned, use LIMIT 10
                    - Return only the SQL query
                    SQL:"""
        response = model.invoke(prompt)
        state.sql_query = clean_sql(response.content)
    except Exception as e:
        state.error = f"SQL generation error: {str(e)}"
        state.sql_query = ""
    return state

def execute(state):
    try:
        if state.error or not state.sql_query:
            return state
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute(state.sql_query)
        state.sql_data = cursor.fetchall()
        cursor.close()
        conn.close()
    except Exception as e:
        state.error = f"Execution error: {str(e)}"
        state.sql_data = []
    return state

def present(state):
    try:
        if state.error:
            state.result = f"Error: {state.error}"
            return state
        if not state.sql_data:
            state.result = "No results found."
            return state
        model = choose_llm("low")
        prompt = f"""Present these results clearly:
                    USER QUERY: {state.tuned_user_query}
                    RESULTS: {state.sql_data}
                    Make it easy to read and natural:"""

        response = model.invoke(prompt)
        state.result = response.content.strip()
    except Exception as e:
        state.result = "Could not format results."
    return state

def get_schema():
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", "4000")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
    )

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT TABLE_NAME, COLUMN_NAME, COLUMN_TYPE,
               IS_NULLABLE, COLUMN_KEY, EXTRA
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = DATABASE()
        ORDER BY TABLE_NAME, ORDINAL_POSITION
    """)

    rows = cursor.fetchall()
    tables = {}

    for row in rows:
        name = row["TABLE_NAME"]
        if name not in tables:
            tables[name] = {"table_name": name, "columns": []}

        tables[name]["columns"].append({
            "name": row["COLUMN_NAME"],
            "type": row["COLUMN_TYPE"],
            "nullable": row["IS_NULLABLE"] == "YES",
            "key": row["COLUMN_KEY"] or None,
            "extra": row["EXTRA"] or None
        })

    cursor.close()
    connection.close()

    return list(tables.values())
