import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

def choose_llm(level: str):
    level = level.lower()
    if (level == 'high'):
        return ChatGroq(model="qwen/qwen3.8-27b", temperature=0)
    elif (level == 'low'):
        return ChatGroq(model="openai/gpt-oss-20b", temperature=0)
    return None
