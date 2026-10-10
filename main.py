#!/usr/bin/env python3
"""
Main Application Entrypoint for the To-Do List Manager CLI.
Initializes persistent storage, business manager, and starts the CLI loop.
"""

import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from todo.storage import JSONTaskStorage
from todo.manager import TaskManager
from todo.models import Priority
from todo.cli import TodoCLI


def seed_sample_data_if_empty(manager: TaskManager) -> None:
    """Preloads realistic sample tasks on first launch for immediate evaluation."""
    if len(manager.list_tasks()) == 0:
        manager.add_task(
            title="Complete Python CLI Internship Assignment",
            description="Build modular To-Do list manager with OOP design and unit tests.",
            priority=Priority.HIGH,
            category="Internship",
            due_date="2026-10-15",
        )
        manager.add_task(
            title="Review Python Data Structures",
            description="Brush up on lists, dictionaries, tuples, and sets in Python 3.",
            priority=Priority.MEDIUM,
            category="Study",
            due_date="2026-10-18",
        )
        manager.add_task(
            title="Submit Week 1 Documentation",
            description="Generate and upload DOCX report and GitHub project URL to Yuva portal.",
            priority=Priority.HIGH,
            category="Internship",
            due_date="2026-10-12",
        )
        task4 = manager.add_task(
            title="Set Up Git Repository",
            description="Initialize python-internship repo and configure remote origin.",
            priority=Priority.LOW,
            category="DevOps",
            due_date="2026-10-10",
        )
        manager.mark_completed(task4.id)


def main() -> None:
    # Ensure data directory exists
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    os.makedirs(data_dir, exist_ok=True)
    storage_path = os.path.join(data_dir, "tasks.json")

    storage = JSONTaskStorage(file_path=storage_path)
    manager = TaskManager(storage=storage)

    # Seed sample tasks if newly initialized
    seed_sample_data_if_empty(manager)

    # Launch CLI
    cli = TodoCLI(manager=manager)
    cli.run()


if __name__ == "__main__":
    main()
