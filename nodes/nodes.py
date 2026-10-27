import mysql.connector
import os
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

def tune_user_query(state: State):
    model = choose_llm("low")
    response = model.invoke(f"convert this message into clear defined message and give me just output don't add any extra details futher it is prompted to the llm with some context: {state.original_user_query}")
    state.tuned_user_query = response.content
    return state

def database_context(state: State):
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(dictionary=True)

    try:
        context = {}

        cursor.execute("SELECT DATABASE() AS database_name")
        context["database"] = cursor.fetchone()["database_name"]

        cursor.execute("SHOW TABLES")
        tables = [
            row[f"Tables_in_{config['database']}"]
            for row in cursor.fetchall()
        ]

        for table in tables:
            cursor.execute(f"DESCRIBE `{table}`")
            columns = cursor.fetchall()

            cursor.execute(f"SELECT COUNT(*) AS total_rows FROM `{table}`")
            count = cursor.fetchone()["total_rows"]

            cursor.execute(f"SELECT * FROM `{table}` LIMIT 5")
            rows = cursor.fetchall()

            context[table] = {
                "columns": columns,
                "total_rows": count,
                "sample_rows": rows
            }
        state.database_context = context

    finally:
        cursor.close()
        conn.close()

    return state

def sql_query(state: State):
    model = choose_llm("high")
    response = model.invoke(f"generate an sql query based on the context: {state.database_context} and user query: {state.tuned_user_query} just give the query to generate nothing else just query if user does not mention the count keep it to limit 10.")
    state.sql_query = response.content
    return state

def execute(state: State):
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(state.sql_query)
        state.sql_data = cursor.fetchall()
        return state
    finally:
        cursor.close()
        conn.close()

def present(state: State):
    model = choose_llm("low")
    response = model.invoke(f"based on this information: {state.sql_data} and user query: {state.tuned_user_query} present to the one in proper way and give direct answers clealy in text formate not any extra just information.")
    state.result = response.content
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

    try:
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
                tables[name] = {
                    "table_name": name,
                    "columns": []
                }

            tables[name]["columns"].append({
                "name": row["COLUMN_NAME"],
                "type": row["COLUMN_TYPE"],
                "nullable": row["IS_NULLABLE"] == "YES",
                "key": row["COLUMN_KEY"] or None,
                "extra": row["EXTRA"] or None
            })

        return list(tables.values())


    finally:
        cursor.close()
        connection.close()
