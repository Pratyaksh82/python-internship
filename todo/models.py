"""
Domain models for the To-Do List Manager application.
Defines Task entities, Priority levels, and Status enumerations.
"""

from enum import Enum
from datetime import datetime
from typing import Optional, Dict, Any


class Priority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

    @classmethod
    def from_string(cls, value: str) -> "Priority":
        """Converts user input into a valid Priority enum or defaults to MEDIUM."""
        if not value:
            return cls.MEDIUM
        cleaned = value.strip().upper()
        for member in cls:
            if member.value == cleaned:
                return member
        return cls.MEDIUM


class TaskStatus(str, Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"


class Task:
    """
    Represents an individual Task entity with metadata.
    Follows OOP encapsulation principles.
    """

    def __init__(
        self,
        task_id: int,
        title: str,
        description: str = "",
        priority: Priority = Priority.MEDIUM,
        status: TaskStatus = TaskStatus.PENDING,
        category: str = "General",
        due_date: Optional[str] = None,
        created_at: Optional[str] = None,
        completed_at: Optional[str] = None,
    ):
        if not title or not title.strip():
            raise ValueError("Task title cannot be empty or whitespace.")

        self.id = task_id
        self.title = title.strip()
        self.description = description.strip() if description else ""
        self.priority = priority if isinstance(priority, Priority) else Priority.from_string(str(priority))
        self.status = status if isinstance(status, TaskStatus) else TaskStatus(status)
        self.category = category.strip() if category else "General"
        self.due_date = due_date.strip() if due_date else None
        self.created_at = created_at or datetime.now().isoformat()
        self.completed_at = completed_at

    def mark_completed(self) -> None:
        """Marks the task as completed and records the completion timestamp."""
        self.status = TaskStatus.COMPLETED
        self.completed_at = datetime.now().isoformat()

    def mark_pending(self) -> None:
        """Resets the task status to pending and clears completion timestamp."""
        self.status = TaskStatus.PENDING
        self.completed_at = None

    @property
    def is_completed(self) -> bool:
        """Returns True if the task is completed."""
        return self.status == TaskStatus.COMPLETED

    def to_dict(self) -> Dict[str, Any]:
        """Serializes the Task instance into a standard dictionary for persistence."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority.value,
            "status": self.status.value,
            "category": self.category,
            "due_date": self.due_date,
            "created_at": self.created_at,
            "completed_at": self.completed_at,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Task":
        """Deserializes a dictionary into a Task instance."""
        return cls(
            task_id=data["id"],
            title=data["title"],
            description=data.get("description", ""),
            priority=Priority.from_string(data.get("priority", "MEDIUM")),
            status=TaskStatus(data.get("status", "PENDING")),
            category=data.get("category", "General"),
            due_date=data.get("due_date"),
            created_at=data.get("created_at"),
            completed_at=data.get("completed_at"),
        )

    def __repr__(self) -> str:
        status_icon = "✓" if self.is_completed else "○"
        return (
            f"Task(id={self.id}, [{status_icon}] title='{self.title}', "
            f"priority={self.priority.value}, category='{self.category}')"
        )
