from pydantic import BaseModel


class DashboardResponse(BaseModel):
    name: str
    total_habits: int
    total_progress_entries: int