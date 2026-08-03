from typing import Optional
from uuid import UUID
from pydantic import BaseModel

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectInDBBase(ProjectBase):
    id: UUID
    owner_id: UUID

    class Config:
        from_attributes = True

class Project(ProjectInDBBase):
    pass
