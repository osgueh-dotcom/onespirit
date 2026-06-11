from typing import List, Optional
from sqlalchemy.orm import Session
from app.modules.tasks.models import Task
from app.modules.tasks.schemas import TaskCreate, TaskUpdate
from app.core.activity import log_activity
from app.core.database import db_commit_safety

def get_task(db: Session, task_id: str) -> Optional[Task]:
    return db.query(Task).filter(Task.id == task_id, Task.deleted_at == None).first()

def get_tasks_by_project(db: Session, project_id: str) -> List[Task]:
    return db.query(Task).filter(Task.project_id == project_id, Task.deleted_at == None).all()

def get_tasks_by_user(db: Session, user_id: str) -> List[Task]:
    return db.query(Task).filter(Task.assigned_to_id == user_id, Task.deleted_at == None).all()

def create_task(db: Session, task_in: TaskCreate, created_by_id: str) -> Task:
    db_task = Task(
        project_id=task_in.project_id,
        title=task_in.title,
        description=task_in.description,
        due_date=task_in.due_date,
        status=task_in.status,
        priority=task_in.priority,
        assigned_to_id=task_in.assigned_to_id,
        created_by_id=created_by_id
    )
    db.add(db_task)
    db_commit_safety(db)
    db.refresh(db_task)
    
    # Central activity logging
    log_activity(
        db, 
        user_id=created_by_id, 
        action="task_allocated", 
        entity_type="task", 
        entity_id=db_task.id, 
        details={"title": db_task.title, "project_id": str(db_task.project_id)}
    )
    
    return db_task

def update_task(db: Session, db_task: Task, task_in: TaskUpdate) -> Task:
    old_status = db_task.status
    task_data = task_in.model_dump(exclude_unset=True)
    for field, value in task_data.items():
        setattr(db_task, field, value)
    db_commit_safety(db)
    db.refresh(db_task)
    
    # Central activity logging if status changed (e.g. checked to 'done')
    if old_status != db_task.status:
        action = "task_completed" if db_task.status == "done" else "task_status_changed"
        log_activity(
            db, 
            user_id=None, 
            action=action, 
            entity_type="task", 
            entity_id=db_task.id, 
            details={"title": db_task.title, "status": db_task.status, "project_id": str(db_task.project_id)}
        )
        
    return db_task

def delete_task(db: Session, db_task: Task) -> Task:
    db_task.soft_delete()
    db_commit_safety(db)
    return db_task
