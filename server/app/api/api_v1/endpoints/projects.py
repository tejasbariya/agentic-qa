from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas
from app.api import deps
from app.models.user import User
from app.models.project import Project

router = APIRouter()

@router.post("/", response_model=schemas.Project)
def create_project(
    *,
    db: Session = Depends(deps.get_db),
    project_in: schemas.ProjectCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    project = Project(
        name=project_in.name,
        description=project_in.description,
        owner_id=current_user.id
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

@router.get("/", response_model=List[schemas.Project])
def read_projects(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    projects = db.query(Project).filter(Project.owner_id == current_user.id).all()
    return projects
