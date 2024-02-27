from typing import Dict, List, Any

from pydantic import BaseModel

class Request(BaseModel):
    users: Dict[str, Any]
    k_recs: int
    n_users_in_project: int


class Responce(BaseModel):
    users: Dict[int, List[int]]
    projects: Dict[int, Any]