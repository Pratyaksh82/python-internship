"""
Storage layer for To-Do List Manager.
Provides persistence abstraction and atomic JSON file storage.
"""

import json
import os
from abc import ABC, abstractmethod
from typing import List
from .models import Task


class TaskStorage(ABC):
    """Abstract persistence interface decoupling business logic from file I/O."""

    @abstractmethod
    def load_tasks(self) -> List[Task]:
        """Loads and returns all stored tasks."""
        pass

    @abstractmethod
    def save_tasks(self, tasks: List[Task]) -> None:
        """Persists the provided list of tasks."""
        pass


class JSONTaskStorage(TaskStorage):
    """
    Concrete storage implementation persisting tasks in formatted JSON.
    Features atomic writes and corrupted file recovery.
    """

    def __init__(self, file_path: str = "tasks.json"):
        self.file_path = file_path

    def load_tasks(self) -> List[Task]:
        """
        Reads tasks from the JSON file.
        Returns an empty list if the file does not exist or is empty.
        """
        if not os.path.exists(self.file_path):
            return []

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    return []
                data = json.loads(content)
                if not isinstance(data, list):
                    return []
                return [Task.from_dict(item) for item in data]
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            # Handle corrupted JSON gracefully by returning empty list
            print(f"[Warning] Failed to parse {self.file_path} ({e}). Starting with clean state.")
            return []

    def save_tasks(self, tasks: List[Task]) -> None:
        """
        Persists tasks using an atomic write pattern (writing to .tmp and replacing).
        Guarantees that files cannot be partially written or corrupted during crashes.
        """
        parent_dir = os.path.dirname(self.file_path)
        if parent_dir and not os.path.exists(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)

        tmp_path = f"{self.file_path}.tmp"
        payload = [task.to_dict() for task in tasks]

        try:
            with open(tmp_path, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=2, ensure_ascii=False)
            # Atomic replacement on Windows and POSIX
            if os.path.exists(self.file_path):
                os.replace(tmp_path, self.file_path)
            else:
                os.rename(tmp_path, self.file_path)
        except Exception as e:
            if os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except OSError:
                    pass
            raise IOError(f"Failed to persist tasks to {self.file_path}: {e}") from e
