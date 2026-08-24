"""
Schedulify Task Routes

Endpoints:
    GET    /api/tasks           - List student's tasks
    POST   /api/tasks           - Create a task
    PUT    /api/tasks/{id}      - Update a task
    DELETE /api/tasks/{id}      - Delete a task
    POST   /api/tasks/{id}/complete - Mark task complete
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.security import get_current_user
from backend.schemas import TaskCreate, TaskUpdate, TaskResponse
from models.user import User, UserRole
from models.student import Student
from models.task import Task, TaskStatus, TaskPriority

router = APIRouter(
    prefix="/api/tasks",
    tags=["Tasks"],
)


def _get_student(user: User, db: Session) -> Student:
    """Ensures user is a student and returns their profile."""
    if user.role != UserRole.STUDENT:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only students can manage tasks.",
        )
    student = (
        db.query(Student)
        .filter(Student.user_id == user.id)
        .first()
    )
    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student profile not found.",
        )
    return student


@router.get("", response_model=list[TaskResponse])
def list_tasks(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List all tasks for the current student."""
    student = _get_student(current_user, db)

    tasks = (
        db.query(Task)
        .filter(Task.student_id == student.id)
        .order_by(Task.due_date)
        .all()
    )

    return [_task_to_response(t) for t in tasks]


@router.post("", response_model=TaskResponse, status_code=201)
def create_task(
    body: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new task."""
    student = _get_student(current_user, db)

    task = Task(
        student_id=student.id,
        title=body.title,
        description=body.description,
        category=body.category,
        priority=TaskPriority(body.priority),
        estimated_duration=body.estimated_duration,
        due_date=body.due_date,
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return _task_to_response(task)


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    body: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update an existing task."""
    student = _get_student(current_user, db)

    task = (
        db.query(Task)
        .filter(
            Task.id == task_id,
            Task.student_id == student.id,
        )
        .first()
    )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found.",
        )

    update_data = body.model_dump(exclude_unset=True)

    if "priority" in update_data and update_data["priority"]:
        update_data["priority"] = TaskPriority(
            update_data["priority"]
        )

    if "status" in update_data and update_data["status"]:
        update_data["status"] = TaskStatus(
            update_data["status"]
        )

    for key, value in update_data.items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)

    return _task_to_response(task)


@router.delete("/{task_id}", status_code=204)
def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a task."""
    student = _get_student(current_user, db)

    task = (
        db.query(Task)
        .filter(
            Task.id == task_id,
            Task.student_id == student.id,
        )
        .first()
    )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found.",
        )

    db.delete(task)
    db.commit()


@router.post("/{task_id}/complete", response_model=TaskResponse)
def complete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Mark a task as completed."""
    student = _get_student(current_user, db)

    task = (
        db.query(Task)
        .filter(
            Task.id == task_id,
            Task.student_id == student.id,
        )
        .first()
    )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found.",
        )

    task.status = TaskStatus.COMPLETED
    db.commit()
    db.refresh(task)

    return _task_to_response(task)


def _task_to_response(task: Task) -> dict:
    """Converts a Task model to a response dict."""
    return TaskResponse(
        id=task.id,
        student_id=task.student_id,
        title=task.title,
        description=task.description,
        category=task.category,
        priority=task.priority.value,
        estimated_duration=task.estimated_duration,
        due_date=task.due_date,
        status=task.status.value,
        created_at=task.created_at,
        updated_at=task.updated_at,
    )
