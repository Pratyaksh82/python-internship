"""
Interactive Command-Line Interface (CLI) for the To-Do List Manager.
Provides menu-driven interaction, tabular formatting, robust input validation,
and graceful exception handling.
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from typing import List, Optional
from .models import Task, Priority, TaskStatus
from .manager import TaskManager, TaskNotFoundError


class TodoCLI:
    """
    Console user interface orchestrating user prompts, table rendering,
    and command dispatching.
    """

    def __init__(self, manager: Optional[TaskManager] = None):
        self.manager = manager or TaskManager()

    def run(self) -> None:
        """Main interaction loop."""
        self.print_welcome()

        while True:
            try:
                self.print_menu()
                choice = input("👉 Enter your choice [1-12]: ").strip()
                print()

                if choice == "1":
                    self.handle_add_task()
                elif choice == "2":
                    self.handle_list_tasks()
                elif choice == "3":
                    self.handle_list_pending()
                elif choice == "4":
                    self.handle_list_completed()
                elif choice == "5":
                    self.handle_mark_completed()
                elif choice == "6":
                    self.handle_mark_pending()
                elif choice == "7":
                    self.handle_update_task()
                elif choice == "8":
                    self.handle_delete_task()
                elif choice == "9":
                    self.handle_search_tasks()
                elif choice == "10":
                    self.handle_clear_completed()
                elif choice == "11":
                    self.handle_display_statistics()
                elif choice == "12":
                    print("=======================================================================")
                    print("  Thank you for using To-Do List Manager! Stay productive! 🚀          ")
                    print("=======================================================================")
                    break
                else:
                    print("⚠️  Invalid choice! Please select an option between 1 and 12.\n")
            except (KeyboardInterrupt, EOFError):
                print("\n\n[Session Finished] Exiting gracefully. Goodbye!")
                break
            except Exception as e:
                print(f"❌ An unexpected error occurred: {e}\n")

    def print_welcome(self) -> None:
        print("=======================================================================")
        print("       📝 PYTHON TO-DO LIST MANAGER (CLI APPLICATION)                  ")
        print("       Junior Python Developer - Week 1 Certification Project          ")
        print("=======================================================================")

    def print_menu(self) -> None:
        print("-----------------------------------------------------------------------")
        print(" MAIN MENU")
        print("-----------------------------------------------------------------------")
        print(" 1. ➕ Add New Task              7. ✏️  Update Task Details")
        print(" 2. 📋 View All Tasks            8. 🗑️  Delete Task")
        print(" 3. ⏳ View Pending Tasks        9. 🔍 Search Tasks by Keyword")
        print(" 4. ✅ View Completed Tasks      10. 🧹 Clear All Completed Tasks")
        print(" 5. ✔️  Mark Task as Completed    11. 📊 View Productivity Metrics")
        print(" 6. 🔄 Mark Task as Pending      12. 🚪 Exit Application")
        print("-----------------------------------------------------------------------")

    def handle_add_task(self) -> None:
        print("--- ➕ ADD NEW TASK ---")
        title = input("Enter Task Title (required): ").strip()
        if not title:
            print("❌ Error: Task title cannot be empty.\n")
            return

        description = input("Enter Description (optional): ").strip()

        print("Priority levels: [1] LOW  |  [2] MEDIUM  |  [3] HIGH (default: 2)")
        p_in = input("Select Priority [1-3, Enter for Medium]: ").strip()
        priority = {
            "1": Priority.LOW,
            "2": Priority.MEDIUM,
            "3": Priority.HIGH
        }.get(p_in, Priority.MEDIUM)

        category = input("Enter Category (e.g. Work, Study, Personal, default: General): ").strip()
        due_date = input("Enter Due Date (e.g. YYYY-MM-DD, optional): ").strip()

        try:
            task = self.manager.add_task(
                title=title,
                description=description,
                priority=priority,
                category=category or "General",
                due_date=due_date or None,
            )
            print(f"✅ Task #{task.id} added successfully: '{task.title}' [{task.priority.value}]\n")
        except ValueError as e:
            print(f"❌ Validation error: {e}\n")

    def handle_list_tasks(self) -> None:
        print("--- 📋 ALL TASKS ---")
        tasks = self.manager.list_tasks()
        self.render_task_table(tasks)

    def handle_list_pending(self) -> None:
        print("--- ⏳ PENDING TASKS ---")
        tasks = self.manager.list_tasks(status=TaskStatus.PENDING)
        self.render_task_table(tasks)

    def handle_list_completed(self) -> None:
        print("--- ✅ COMPLETED TASKS ---")
        tasks = self.manager.list_tasks(status=TaskStatus.COMPLETED)
        self.render_task_table(tasks)

    def handle_mark_completed(self) -> None:
        print("--- ✔️ MARK TASK AS COMPLETED ---")
        task_id = self.read_int("Enter Task ID to mark completed: ")
        if task_id is None:
            return

        try:
            task = self.manager.mark_completed(task_id)
            print(f"✅ Task #{task.id} marked as COMPLETED! Good job!\n")
        except TaskNotFoundError as e:
            print(f"❌ {e}\n")

    def handle_mark_pending(self) -> None:
        print("--- 🔄 MARK TASK AS PENDING ---")
        task_id = self.read_int("Enter Task ID to reset to pending: ")
        if task_id is None:
            return

        try:
            task = self.manager.mark_pending(task_id)
            print(f"✅ Task #{task.id} reset to PENDING.\n")
        except TaskNotFoundError as e:
            print(f"❌ {e}\n")

    def handle_update_task(self) -> None:
        print("--- ✏️ UPDATE TASK ---")
        task_id = self.read_int("Enter Task ID to update: ")
        if task_id is None:
            return

        try:
            task = self.manager.get_task(task_id)
            print(f"Current Title:       {task.title}")
            print(f"Current Description: {task.description or '(None)'}")
            print(f"Current Priority:    {task.priority.value}")
            print(f"Current Category:    {task.category}")
            print(f"Current Due Date:    {task.due_date or '(None)'}\n")

            new_title = input(f"New Title [Enter to keep '{task.title}']: ").strip()
            new_desc = input("New Description [Enter to keep current]: ").strip()

            p_in = input("New Priority [1: LOW, 2: MEDIUM, 3: HIGH, Enter to keep]: ").strip()
            new_priority = {
                "1": Priority.LOW,
                "2": Priority.MEDIUM,
                "3": Priority.HIGH
            }.get(p_in, None)

            new_cat = input(f"New Category [Enter to keep '{task.category}']: ").strip()
            new_due = input(f"New Due Date [Enter to keep '{task.due_date or ''}']: ").strip()

            updated = self.manager.update_task(
                task_id=task_id,
                title=new_title if new_title else None,
                description=new_desc if new_desc else None,
                priority=new_priority,
                category=new_cat if new_cat else None,
                due_date=new_due if new_due else None,
            )
            print(f"✅ Task #{updated.id} updated successfully!\n")
        except TaskNotFoundError as e:
            print(f"❌ {e}\n")
        except ValueError as e:
            print(f"❌ Validation error: {e}\n")

    def handle_delete_task(self) -> None:
        print("--- 🗑️ DELETE TASK ---")
        task_id = self.read_int("Enter Task ID to delete: ")
        if task_id is None:
            return

        try:
            task = self.manager.get_task(task_id)
            confirm = input(f"⚠️ Are you sure you want to delete Task #{task.id} '{task.title}'? (y/N): ").strip()
            if confirm.lower() in ("y", "yes"):
                self.manager.remove_task(task_id)
                print(f"✅ Task #{task_id} deleted successfully.\n")
            else:
                print("ℹ️ Deletion cancelled.\n")
        except TaskNotFoundError as e:
            print(f"❌ {e}\n")

    def handle_search_tasks(self) -> None:
        print("--- 🔍 SEARCH TASKS ---")
        keyword = input("Enter search keyword (title/description/category): ").strip()
        if not keyword:
            print("❌ Keyword cannot be empty.\n")
            return

        matches = self.manager.search_tasks(keyword)
        if not matches:
            print(f"ℹ️ No tasks found matching '{keyword}'.\n")
        else:
            print(f"✅ Found {len(matches)} matching task(s):")
            self.render_task_table(matches)

    def handle_clear_completed(self) -> None:
        print("--- 🧹 CLEAR COMPLETED TASKS ---")
        confirm = input("⚠️ Are you sure you want to remove ALL completed tasks? (y/N): ").strip()
        if confirm.lower() in ("y", "yes"):
            count = self.manager.clear_completed()
            print(f"✅ Cleared {count} completed task(s).\n")
        else:
            print("ℹ️ Operation cancelled.\n")

    def handle_display_statistics(self) -> None:
        print("--- 📊 PRODUCTIVITY METRICS ---")
        stats = self.manager.get_statistics()
        print(f"Total Tasks:          {stats['total']}")
        print(f"Completed Tasks:      {stats['completed']}")
        print(f"Pending Tasks:        {stats['pending']}")
        print(f"Completion Rate:      {stats['completion_rate']}%")
        print("Priority Breakdown:")
        for prio, cnt in stats["by_priority"].items():
            print(f" - {prio:<8}: {cnt}")
        print()

    def render_task_table(self, tasks: List[Task]) -> None:
        if not tasks:
            print("ℹ️ No tasks to display.\n")
            return

        print("+-----+--------+--------------------------------+----------+------------+------------+")
        print("| ID  | Status | Title                          | Priority | Category   | Due Date   |")
        print("+-----+--------+--------------------------------+----------+------------+------------+")

        for t in tasks:
            status_symbol = "[✓]" if t.is_completed else "[ ]"
            title_trunc = t.title[:30] if len(t.title) <= 30 else t.title[:27] + "..."
            cat_trunc = t.category[:10] if len(t.category) <= 10 else t.category[:8] + ".."
            due_str = t.due_date if t.due_date else "-"

            print(f"| {t.id:<3} | {status_symbol:^6} | {title_trunc:<30} | {t.priority.value:<8} | {cat_trunc:<10} | {due_str:<10} |")

        print("+-----+--------+--------------------------------+----------+------------+------------+")
        print(f"Total: {len(tasks)} task(s)\n")

    def read_int(self, prompt: str) -> Optional[int]:
        raw = input(prompt).strip()
        try:
            return int(raw)
        except ValueError:
            print("❌ Invalid input! Please enter a valid numeric ID.\n")
            return None
