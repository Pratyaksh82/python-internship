"""
Comprehensive unit test suite for the To-Do List Manager application.
Utilizes Python standard library's unittest framework.
"""

import os
import shutil
import tempfile
import unittest
from todo.models import Task, Priority, TaskStatus
from todo.storage import JSONTaskStorage
from todo.manager import TaskManager, TaskNotFoundError


class TestTaskModel(unittest.TestCase):
    """Tests for the Task entity model."""

    def test_create_valid_task(self):
        task = Task(task_id=1, title="Test Task", description="Sample description", priority=Priority.HIGH)
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "Sample description")
        self.assertEqual(task.priority, Priority.HIGH)
        self.assertEqual(task.status, TaskStatus.PENDING)
        self.assertFalse(task.is_completed)

    def test_empty_title_raises_value_error(self):
        with self.assertRaises(ValueError):
            Task(task_id=1, title="")
        with self.assertRaises(ValueError):
            Task(task_id=1, title="   ")

    def test_mark_completed_and_pending(self):
        task = Task(task_id=1, title="Task Lifecycle")
        self.assertFalse(task.is_completed)
        self.assertIsNone(task.completed_at)

        task.mark_completed()
        self.assertTrue(task.is_completed)
        self.assertIsNotNone(task.completed_at)

        task.mark_pending()
        self.assertFalse(task.is_completed)
        self.assertIsNone(task.completed_at)

    def test_serialization_round_trip(self):
        original = Task(
            task_id=42,
            title="Serialized Task",
            description="Detail",
            priority=Priority.LOW,
            category="Work",
            due_date="2026-10-31",
        )
        data = original.to_dict()
        restored = Task.from_dict(data)

        self.assertEqual(original.id, restored.id)
        self.assertEqual(original.title, restored.title)
        self.assertEqual(original.description, restored.description)
        self.assertEqual(original.priority, restored.priority)
        self.assertEqual(original.category, restored.category)
        self.assertEqual(original.due_date, restored.due_date)


class TestJSONStorage(unittest.TestCase):
    """Tests for JSON persistence storage."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.storage_file = os.path.join(self.test_dir, "test_tasks.json")
        self.storage = JSONTaskStorage(file_path=self.storage_file)

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_load_non_existent_file_returns_empty_list(self):
        tasks = self.storage.load_tasks()
        self.assertEqual(tasks, [])

    def test_save_and_load_tasks(self):
        t1 = Task(task_id=1, title="Task One", priority=Priority.HIGH)
        t2 = Task(task_id=2, title="Task Two", priority=Priority.LOW)

        self.storage.save_tasks([t1, t2])
        loaded = self.storage.load_tasks()

        self.assertEqual(len(loaded), 2)
        self.assertEqual(loaded[0].title, "Task One")
        self.assertEqual(loaded[1].title, "Task Two")

    def test_corrupted_json_handled_gracefully(self):
        with open(self.storage_file, "w", encoding="utf-8") as f:
            f.write("{invalid json syntax!!!")

        loaded = self.storage.load_tasks()
        self.assertEqual(loaded, [])


class TestTaskManager(unittest.TestCase):
    """Tests for TaskManager business logic and workflows."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.storage_file = os.path.join(self.test_dir, "manager_tasks.json")
        self.storage = JSONTaskStorage(file_path=self.storage_file)
        self.manager = TaskManager(storage=self.storage)

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_add_task_success(self):
        task = self.manager.add_task(title="Build Feature", priority=Priority.HIGH, category="Dev")
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Build Feature")
        self.assertEqual(len(self.manager.list_tasks()), 1)

    def test_auto_incrementing_ids(self):
        t1 = self.manager.add_task(title="First")
        t2 = self.manager.add_task(title="Second")
        t3 = self.manager.add_task(title="Third")
        self.assertEqual(t1.id, 1)
        self.assertEqual(t2.id, 2)
        self.assertEqual(t3.id, 3)

    def test_get_task_success_and_not_found(self):
        t = self.manager.add_task(title="Existing")
        found = self.manager.get_task(t.id)
        self.assertEqual(found.title, "Existing")

        with self.assertRaises(TaskNotFoundError):
            self.manager.get_task(999)

    def test_filtering_tasks_by_status(self):
        t1 = self.manager.add_task(title="Task A")
        t2 = self.manager.add_task(title="Task B")
        self.manager.mark_completed(t1.id)

        pending = self.manager.list_tasks(status=TaskStatus.PENDING)
        completed = self.manager.list_tasks(status=TaskStatus.COMPLETED)

        self.assertEqual(len(pending), 1)
        self.assertEqual(pending[0].id, t2.id)
        self.assertEqual(len(completed), 1)
        self.assertEqual(completed[0].id, t1.id)

    def test_sorting_by_priority(self):
        self.manager.add_task(title="Low Item", priority=Priority.LOW)
        self.manager.add_task(title="High Item", priority=Priority.HIGH)
        self.manager.add_task(title="Medium Item", priority=Priority.MEDIUM)

        sorted_tasks = self.manager.list_tasks(sort_by="priority")
        self.assertEqual(sorted_tasks[0].priority, Priority.HIGH)
        self.assertEqual(sorted_tasks[1].priority, Priority.MEDIUM)
        self.assertEqual(sorted_tasks[2].priority, Priority.LOW)

    def test_update_task(self):
        task = self.manager.add_task(title="Original Title", priority=Priority.LOW)
        updated = self.manager.update_task(
            task_id=task.id,
            title="Updated Title",
            description="New description",
            priority=Priority.HIGH,
            category="Work",
            due_date="2026-12-01",
        )
        self.assertEqual(updated.title, "Updated Title")
        self.assertEqual(updated.description, "New description")
        self.assertEqual(updated.priority, Priority.HIGH)
        self.assertEqual(updated.category, "Work")
        self.assertEqual(updated.due_date, "2026-12-01")

    def test_remove_task(self):
        task = self.manager.add_task(title="To Delete")
        self.assertEqual(len(self.manager.list_tasks()), 1)

        deleted = self.manager.remove_task(task.id)
        self.assertEqual(deleted.title, "To Delete")
        self.assertEqual(len(self.manager.list_tasks()), 0)

        with self.assertRaises(TaskNotFoundError):
            self.manager.get_task(task.id)

    def test_search_tasks(self):
        self.manager.add_task(title="Write Python Code", description="Backend", category="Engineering")
        self.manager.add_task(title="Review Documentation", description="Manual", category="Admin")
        self.manager.add_task(title="Python Unit Tests", description="Quality", category="Engineering")

        matches = self.manager.search_tasks("python")
        self.assertEqual(len(matches), 2)

        eng_matches = self.manager.search_tasks("engineering")
        self.assertEqual(len(eng_matches), 2)

        no_matches = self.manager.search_tasks("nonexistent")
        self.assertEqual(len(no_matches), 0)

    def test_clear_completed(self):
        t1 = self.manager.add_task(title="Task 1")
        t2 = self.manager.add_task(title="Task 2")
        t3 = self.manager.add_task(title="Task 3")
        self.manager.mark_completed(t1.id)
        self.manager.mark_completed(t3.id)

        cleared_count = self.manager.clear_completed()
        self.assertEqual(cleared_count, 2)
        remaining = self.manager.list_tasks()
        self.assertEqual(len(remaining), 1)
        self.assertEqual(remaining[0].id, t2.id)

    def test_statistics(self):
        t1 = self.manager.add_task(title="High 1", priority=Priority.HIGH)
        t2 = self.manager.add_task(title="Medium 1", priority=Priority.MEDIUM)
        t3 = self.manager.add_task(title="Low 1", priority=Priority.LOW)
        self.manager.mark_completed(t1.id)

        stats = self.manager.get_statistics()
        self.assertEqual(stats["total"], 3)
        self.assertEqual(stats["completed"], 1)
        self.assertEqual(stats["pending"], 2)
        self.assertEqual(stats["completion_rate"], 33.3)
        self.assertEqual(stats["by_priority"]["HIGH"], 1)
        self.assertEqual(stats["by_priority"]["MEDIUM"], 1)
        self.assertEqual(stats["by_priority"]["LOW"], 1)


if __name__ == "__main__":
    unittest.main()
