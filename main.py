from langgraph.graph import StateGraph, START, END
from nodes.nodes import tune_user_query, database_context, sql_query, execute, present
from model.state import State

def main(user_query: str):

    graph = StateGraph(State)

    graph.add_node("tune_user_query", tune_user_query)
    graph.add_node("database_context", database_context)
    graph.add_node("sql_query", sql_query)
    graph.add_node("execute", execute)
    graph.add_node("present", present)

    graph.add_edge(START, "tune_user_query")
    graph.add_edge("tune_user_query", "database_context")
    graph.add_edge("database_context", "sql_query")
    graph.add_edge("sql_query", "execute")
    graph.add_edge("execute", "present")
    graph.add_edge("present", END)

    app = graph.compile()

    result = app.invoke(State(
        original_user_query = user_query,
        tuned_user_query = "",
        database_context = {},
        sql_query = "",
        sql_data = "",
        result = ""
    ))

    return result
