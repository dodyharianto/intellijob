from pydantic import BaseModel
from typing import List, Optional

class JobResult(BaseModel):
    title: str
    company: str
    location: str
    link: str
    description: str
    salary: Optional[str] = None
    posted_at: Optional[str] = None