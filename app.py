from fastapi import FastAPI
from pydantic import BaseModel
from main import main
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from nodes.nodes import get_schema

app = FastAPI(title="QueryBite API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)

def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )

@app.post("/query")
def query_database(request: QueryRequest):
    result = main(request.query)
    return {"result": result["result"]}

@app.get("/schema")
def schema_endpoint():
    return get_schema()
