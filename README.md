# BaseInterface

### An AI-Powered Natural Language Database Interface

BaseInterface is a mini project that allows users to interact with a MySQL database using natural language instead of writing SQL queries manually. It combines Python, FastAPI, LangGraph, and Large Language Models (LLMs) to understand user questions, generate SQL queries, execute them against a database, and present the results in a conversational interface.

The project also provides an API endpoint to retrieve database table schemas, making it easier to inspect database structures programmatically.

> **Project type:** Mini Project
> **Category:** Artificial Intelligence · Backend Development · Database Systems
> **Status:** Development
> **Project name:** BaseInterface

---

## Table of Contents

- [BaseInterface](#baseinterface)
    - [An AI-Powered Natural Language Database Interface](#an-ai-powered-natural-language-database-interface)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Problem Statement](#problem-statement)
  - [Objectives](#objectives)
  - [Features](#features)
    - [1. Natural Language to SQL](#1-natural-language-to-sql)
    - [2. AI-Powered Query Processing](#2-ai-powered-query-processing)
    - [3. Database Schema Retrieval](#3-database-schema-retrieval)
    - [4. SQL Execution](#4-sql-execution)
    - [5. Conversational Results](#5-conversational-results)
    - [6. Chat-Based User Interface](#6-chat-based-user-interface)
    - [7. REST API](#7-rest-api)
  - [How It Works](#how-it-works)
    - [Workflow stages](#workflow-stages)
  - [Technology Stack](#technology-stack)
  - [Project Structure](#project-structure)
  - [API Endpoints](#api-endpoints)
    - [`GET /`](#get-)
    - [`POST /query`](#post-query)
    - [`GET /schema`](#get-schema)
    - [`GET /docs`](#get-docs)
  - [Installation and Setup](#installation-and-setup)
    - [Prerequisites](#prerequisites)
    - [Step 1: Clone the repository](#step-1-clone-the-repository)
    - [Step 2: Create the environment](#step-2-create-the-environment)
    - [Step 3: Configure environment variables](#step-3-configure-environment-variables)
    - [Step 4: Verify the database connection](#step-4-verify-the-database-connection)
    - [Step 5: Start the application](#step-5-start-the-application)
  - [Environment Configuration](#environment-configuration)
  - [Example Usage](#example-usage)
  - [These are example prompts, not guaranteed results. The generated SQL must match the actual schema, and the corresponding tables and columns must exist in the configured database.](#these-are-example-prompts-not-guaranteed-results-the-generated-sql-must-match-the-actual-schema-and-the-corresponding-tables-and-columns-must-exist-in-the-configured-database)

---

## Overview

Working with databases often requires knowledge of SQL, including `SELECT` queries, filtering, sorting, aggregation, joins, and relationships between tables.

BaseInterface aims to simplify this process by allowing users to ask questions in plain English. The AI-powered workflow interprets the question, uses database schema information as context, generates an SQL query, executes it, and returns a human-readable answer.

For example, instead of writing:

```sql
SELECT COUNT(*) FROM customer;
```

A user can ask:

```text
How many customers are in the database?
```

BaseInterface processes the question and returns the corresponding result through its chat interface.

## Problem Statement

Users who are unfamiliar with SQL may find it difficult to retrieve information from relational databases. Even experienced developers must repeatedly write queries for routine data exploration.

The goal of BaseInterface is to build a simple natural-language interface between users and a relational database, combining AI-driven query generation with a Python backend and a browser-based user interface.

## Objectives

- Allow users to query a database using natural language.
- Use an LLM to interpret user questions and generate SQL.
- Retrieve database schema information to provide context for query generation.
- Execute generated SQL and collect the results.
- Present results in a conversational format.
- Expose database schema information through a REST API.
- Understand how AI workflows integrate with backend applications and databases.

## Features

### 1. Natural Language to SQL

Users can ask questions without manually writing SQL. The AI workflow interprets the question and generates a database query.

### 2. AI-Powered Query Processing

The application uses a LangGraph workflow to organize the query-processing steps into separate stages.

### 3. Database Schema Retrieval

The application retrieves table and column information from MySQL's `INFORMATION_SCHEMA`, including data types, nullability, key information, and additional column properties.

### 4. SQL Execution

Generated SQL is executed against the configured database, and the returned rows are passed to the result-processing stage.

### 5. Conversational Results

The final database results are processed into a user-friendly response using an LLM.

### 6. Chat-Based User Interface

The browser interface provides a conversational experience with a message composer, suggested queries, response indicators, and recent questions.

### 7. REST API

FastAPI exposes endpoints for the chat interface and database schema retrieval.

---

## How It Works

The application follows a multi-stage AI workflow.

```text
User Question
     |
     v
Query Understanding
     |
     v
Database Schema and Context
     |
     v
AI-Generated SQL
     |
     v
Database Execution
     |
     v
AI Result Presentation
     |
     v
Final Answer to User
```

### Workflow stages

1. **Query understanding:** An LLM refines the user's original question into a clearer database-related request.
2. **Schema retrieval:** The application gathers information about available tables, columns, and sample records.
3. **SQL generation:** An LLM uses the question and database context to generate an SQL query.
4. **Execution:** Python connects to the database and executes the generated query.
5. **Result presentation:** An LLM converts the query output into a readable response.
6. **API response:** FastAPI returns the result to the frontend, which displays it in the chat.

LangGraph manages the workflow state and coordinates the processing stages.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| FastAPI | REST API and HTTP routing |
| LangGraph | Multi-stage AI workflow orchestration |
| Large Language Models | Question interpretation, SQL generation, and result presentation |
| Groq API, if configured | Access to supported hosted LLMs |
| MySQL | Relational database |
| `mysql-connector-python` | Python-to-MySQL connectivity |
| Pydantic | Workflow state and request validation |
| Jinja2 | Rendering the HTML template through FastAPI |
| HTML | Chat interface structure |
| CSS | Styling and responsive layout |
| JavaScript | Sending queries and displaying responses |
| `python-dotenv` | Loading environment variables |
| `uv` | Python dependency and virtual environment management |
| Uvicorn | ASGI server for FastAPI |

*The exact LLM provider and model depend on the configuration in the application.*

## Project Structure

```text
baseinterface/
├── app.py                 # FastAPI application and API endpoints
├── main.py                # LangGraph workflow and query processing
├── database.py            # Database schema retrieval function
├── templates/
│   └── index.html         # Chat interface
├── .env                   # Database and LLM configuration
├── .gitignore             # Files excluded from version control
├── pyproject.toml         # Project dependencies and metadata
├── uv.lock                # Locked dependency versions, if generated
└── README.md              # Project documentation
```

The structure may vary depending on the current organization of the code.

## API Endpoints

### `GET /`

Serves the browser-based chat interface.

**Example:**

```text
http://127.0.0.1:8000/
```

### `POST /query`

Accepts a natural-language question, runs the AI workflow, and returns the result.

**Request body:**

```json
{
  "query": "Show all customers"
}
```

**Example response:**

```json
{
  "result": "Here are the customers in your database..."
}
```

The actual response depends on the question and database contents.

### `GET /schema`

Returns the database name, total number of tables, and schema details for each table.

**Example:**

```text
http://127.0.0.1:8000/schema
```

**Example response:**

```json
{
  "database": "foody",
  "total_tables": 1,
  "tables": [
    {
      "table_name": "customer",
      "columns": [
        {
          "name": "customer_id",
          "type": "bigint",
          "nullable": false,
          "key": "PRI",
          "extra": "auto_increment"
        }
      ]
    }
  ]
}
```

This is an illustrative response. Actual table names and columns depend on the configured database.

### `GET /docs`

Opens FastAPI's interactive API documentation, where supported endpoints can be tested.

```text
http://127.0.0.1:8000/docs
```

---

## Installation and Setup

### Prerequisites

Install the following before running the project:

- Python 3.11 or a compatible version supported by the selected dependencies.
- `uv` Python package manager.
- Access to a MySQL-compatible database.
- An API key for the LLM provider used in the project.

### Step 1: Clone the repository

Replace the placeholder with your actual repository URL.

```bash
git clone <YOUR_REPOSITORY_URL>
cd baseinterface
```

Alternatively, navigate directly to the project directory if you already have the source code.

### Step 2: Create the environment

```bash
uv sync
```

If the project does not yet have its dependencies defined, initialize it and install the required packages:

```bash
uv init
uv add fastapi uvicorn jinja2
uv add langgraph pydantic mysql-connector-python python-dotenv
```

Install the LLM provider's SDK as required by your implementation. For example, if you use Groq's Python SDK directly:

```bash
uv add groq
```

### Step 3: Configure environment variables

Create a `.env` file in the project root. Refer to the configuration section below.

### Step 4: Verify the database connection

Ensure the database is reachable and that the configured user has the necessary permissions to inspect schema metadata and execute the intended queries.

### Step 5: Start the application

```bash
uv run uvicorn app:api --reload
```

Open the following URLs:

- Chat interface: `http://127.0.0.1:8000/`
- Schema endpoint: `http://127.0.0.1:8000/schema`
- API documentation: `http://127.0.0.1:8000/docs`

---

## Environment Configuration

The application reads its configuration from environment variables instead of hardcoding database credentials in the source code.

Example `.env` template:

```dotenv
DB_HOST=your_database_host
DB_PORT=4000
DB_USER=your_database_username
DB_PASSWORD=your_database_password
DB_NAME=foody

GROQ_API_KEY=your_llm_api_key
```

Use the actual variable names expected by your database connection function and LLM configuration. For example, a local MySQL installation commonly uses port `3306`, whereas a hosted database may use a different port.

**Security recommendations:**

- Never commit `.env` to a public repository.
- Add `.env` and `.venv/` to `.gitignore`.
- Do not expose database credentials or LLM API keys in frontend JavaScript.
- Use a database account with restricted permissions.
- Validate AI-generated SQL before executing it.
- Avoid exposing raw database errors and sensitive records to untrusted users.

## Example Usage

After starting the application, open the chat interface and submit questions such as:

```text
Show all customers.
```

```text
How many customers are registered?
```

```text
List the available database tables.
```

```text
Show the latest orders.
```

```text
Find customers from a particular city.
```

These are example prompts, not guaranteed results. The generated SQL must match the actual schema, and the corresponding tables and columns must exist in the configured database.
---
**BaseInterface - Ask questions. Get answers from your database.**
