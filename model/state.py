from pydantic import BaseModel
from typing import Any, Optional

class State(BaseModel):
    original_user_query: str
    tuned_user_query: str = ""
    database_context: dict[str, Any] = {}
    sql_query: str = ""
    sql_data: Any = None
    result: str = ""
    error: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True
