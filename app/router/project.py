import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from typing import List
from fastapi import APIRouter, Depends, status, HTTPException, Response, Query
import database, models
# from sqlalchemy.orm import Session
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select
import oauth2

router = APIRouter(
    tags = ['Projects']
)

###############################################################################
## Project

@router.post('/projects/', response_model=models.ProjectRead)
def create_project(
    *,
    session: Session = Depends(database.get_session),
    current_user: models.User = Depends(oauth2.get_current_user),
    project: models.ProjectCreate
):
    db_project = models.Project.from_orm(project)
    session.add(db_project)
    session.commit()
    session.refresh(db_project)
    return project

@router.get('/projects', response_model=List[models.ProjectRead])
def read_projects(
    *,
    session: Session = Depends(database.get_session),
    current_user: models.User = Depends(oauth2.get_current_user),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
):
    # projects = session.exec(select(models.Project).offset(offset).limit(limit)).all()
    projects = session.query(models.Project).filter(models.Project.author_id == current_user.id).offset(offset).limit(limit).all()
    return projects

@router.get('/projects/{project_id}', response_model=models.ProjectReadWithUser)
def read_project(
    *,
    session: Session = Depends(database.get_session),
    current_user: models.User = Depends(oauth2.get_current_user),
    project_id: int
):
    project = session.get(models.Project, project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Project with id {project_id} is not available")
    return project

@router.patch('/projects/{project_id}', response_model=models.ProjectRead)
def update_project(
    *,
    session: Session = Depends(database.get_session),
    current_user: models.User = Depends(oauth2.get_current_user),
    project_id: int,
    project: models.ProjectUpdate
):
    db_project = session.get(models.Project, project_id)
    if not db_project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Project with id {project_id} not found")
    project_data = project.dict(exclude_unset=True)
    for key, value in project_data.items():
        setattr(db_project, key, value)
    session.add(db_project)
    session.commit()
    session.refresh(db_project)
    return db_project

@router.delete('/projects/{project_id}')
def delete_project(
    *,
    session: Session = Depends(database.get_session),
    current_user: models.User = Depends(oauth2.get_current_user),
    project_id: int,
):
    project = session.get(models.Project, project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Project with id {project_id} not found")
    session.delete(project)
    session.commit()
    return {'detail': f"Project with id {project_id} was deleted"}


###############################################################################
