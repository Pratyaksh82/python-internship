"""
Core business logic layer for the To-Do List Manager.
Orchestrates task CRUD workflows, filtering, searching, and statistical aggregations.
"""

from typing import List, Optional, Dict, Any
from .models import Task, Priority, TaskStatus
from .storage import TaskStorage, JSONTaskStorage


class TaskNotFoundError(Exception):
    """Raised when an operation targets a non-existent task ID."""
    pass


class TaskManager:
    """
    Manages task lifecycle, business validations, and persistence interactions.
    """

    def __init__(self, storage: Optional[TaskStorage] = None):
        self.storage = storage or JSONTaskStorage()
        self._tasks: List[Task] = []
        self._next_id: int = 1
        self.load()

    def load(self) -> None:
        """Loads tasks from persistent storage into memory."""
        self._tasks = self.storage.load_tasks()
        if self._tasks:
            self._next_id = max(task.id for task in self._tasks) + 1
        else:
            self._next_id = 1

    def save(self) -> None:
        """Persists current in-memory tasks to storage."""
        self.storage.save_tasks(self._tasks)

    def add_task(
        self,
        title: str,
        description: str = "",
        priority: Priority = Priority.MEDIUM,
        category: str = "General",
        due_date: Optional[str] = None,
    ) -> Task:
        """
        Creates, validates, and adds a new task.
        """
        if not title or not title.strip():
            raise ValueError("Task title cannot be empty.")

        task = Task(
            task_id=self._next_id,
            title=title,
            description=description,
            priority=priority,
            status=TaskStatus.PENDING,
            category=category,
            due_date=due_date,
        )
        self._next_id += 1
        self._tasks.append(task)
        self.save()
        return task

    def get_task(self, task_id: int) -> Task:
        """
        Retrieves a task by its ID or raises TaskNotFoundError.
        """
        for task in self._tasks:
            if task.id == task_id:
                return task
        raise TaskNotFoundError(f"Task with ID #{task_id} not found.")

    def list_tasks(
        self,
        status: Optional[TaskStatus] = None,
        priority: Optional[Priority] = None,
        category: Optional[str] = None,
        sort_by: Optional[str] = None,
    ) -> List[Task]:
        """
        Returns a filtered and sorted list of tasks.
        """
        results = list(self._tasks)

        if status:
            results = [t for t in results if t.status == status]

        if priority:
            results = [t for t in results if t.priority == priority]

        if category:
            cat_clean = category.strip().lower()
            results = [t for t in results if t.category.lower() == cat_clean]

        if sort_by == "priority":
            # Priority order: HIGH (0), MEDIUM (1), LOW (2)
            priority_rank = {Priority.HIGH: 0, Priority.MEDIUM: 1, Priority.LOW: 2}
            results.sort(key=lambda t: priority_rank.get(t.priority, 1))
        elif sort_by == "due_date":
            # Sort by due_date (None values placed last)
            results.sort(key=lambda t: (t.due_date is None, t.due_date or ""))
        elif sort_by == "title":
            results.sort(key=lambda t: t.title.lower())
        else:
            # Default: order by ID
            results.sort(key=lambda t: t.id)

        return results

    def update_task(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        priority: Optional[Priority] = None,
        category: Optional[str] = None,
        due_date: Optional[str] = None,
    ) -> Task:
        """
        Updates fields of an existing task.
        """
        task = self.get_task(task_id)

        if title is not None:
            if not title.strip():
                raise ValueError("Task title cannot be empty.")
            task.title = title.strip()

        if description is not None:
            task.description = description.strip()

        if priority is not None:
            task.priority = priority if isinstance(priority, Priority) else Priority.from_string(str(priority))

        if category is not None:
            task.category = category.strip() if category else "General"

        if due_date is not None:
            task.due_date = due_date.strip() if due_date else None

        self.save()
        return task

    def mark_completed(self, task_id: int) -> Task:
        """Marks a task as completed."""
        task = self.get_task(task_id)
        task.mark_completed()
        self.save()
        return task

    def mark_pending(self, task_id: int) -> Task:
        """Marks a task as pending."""
        task = self.get_task(task_id)
        task.mark_pending()
        self.save()
        return task

    def remove_task(self, task_id: int) -> Task:
        """Deletes a task by ID."""
        task = self.get_task(task_id)
        self._tasks.remove(task)
        self.save()
        return task

    def search_tasks(self, keyword: str) -> List[Task]:
        """
        Performs case-insensitive substring search on task titles and descriptions.
        """
        if not keyword or not keyword.strip():
            return []
        q = keyword.strip().lower()
        return [
            t for t in self._tasks
            if q in t.title.lower() or q in t.description.lower() or q in t.category.lower()
        ]

    def clear_completed(self) -> int:
        """Removes all completed tasks from inventory. Returns count of deleted tasks."""
        completed_tasks = [t for t in self._tasks if t.is_completed]
        count = len(completed_tasks)
        self._tasks = [t for t in self._tasks if not t.is_completed]
        self.save()
        return count

    def get_statistics(self) -> Dict[str, Any]:
        """Calculates aggregated metrics across all managed tasks."""
        total = len(self._tasks)
        completed = sum(1 for t in self._tasks if t.is_completed)
        pending = total - completed
        rate = (completed / total * 100) if total > 0 else 0.0

        by_priority = {
            Priority.HIGH.value: sum(1 for t in self._tasks if t.priority == Priority.HIGH),
            Priority.MEDIUM.value: sum(1 for t in self._tasks if t.priority == Priority.MEDIUM),
            Priority.LOW.value: sum(1 for t in self._tasks if t.priority == Priority.LOW),
        }

        return {
            "total": total,
            "completed": completed,
            "pending": pending,
            "completion_rate": round(rate, 1),
            "by_priority": by_priority,
        }
