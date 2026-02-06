import logging

from core.logger import setup_logger
from core.user_input import get_user_details, ask_user_choice
from core.memory import load_memory, save_full_state, reset_memory
from core.rules import analyze_goal
from core.planner import generate_tasks
from core.task_manager import initialize_tasks, display_tasks, mark_task_done


def main():
    setup_logger()
    logging.info("Application started")

    memory = load_memory()

    # =========================
    # CASE 1: Existing memory
    # =========================
    if memory:
        name = memory.get("name", "User")
        active_goal = memory.get("goal", "")
        tasks = memory.get("tasks", [])

        print(f"\n👋 Welcome back, {name}")

        print("\n📌 Current Goal:")
        print(active_goal)

        # Intelligence layer
        advice = analyze_goal(active_goal)
        print("\n💡 Advice:")
        print(advice)

        # Planning / Task layer
        if not tasks:
            raw_tasks = generate_tasks(active_goal)
            tasks = initialize_tasks(raw_tasks)
            save_full_state(name, active_goal, tasks)

        display_tasks(tasks)

        # Task update loop
        task_choice = input(
            "\nEnter task number to mark DONE (or press Enter to skip): "
        ).strip()

        if task_choice.isdigit():
            mark_task_done(tasks, int(task_choice) - 1)
            save_full_state(name, active_goal, tasks)
            print("✅ Task marked as DONE")

        # User control options
        choice = ask_user_choice()

        if choice == "2":
            print("\nUpdate your details:")
            new_name, new_goal = get_user_details()
            raw_tasks = generate_tasks(new_goal)
            tasks = initialize_tasks(raw_tasks)
            save_full_state(new_name, new_goal, tasks)
            logging.info("User updated name, goal, and tasks")
            print("✅ Name, goal, and tasks updated")

        elif choice == "3":
            reset_memory()
            logging.info("User reset memory")
            print("🗑️ Memory reset successfully")

        else:
            logging.info("User kept existing state")
            print("➡️ Continuing with current plan")

    # =========================
    # CASE 2: First run
    # =========================
    else:
        logging.info("First run detected")

        name, goal = get_user_details()
        raw_tasks = generate_tasks(goal)
        tasks = initialize_tasks(raw_tasks)

        save_full_state(name, goal, tasks)

        print(f"\n👋 Welcome, {name}")

        print("\n📌 Your Goal:")
        print(goal)

        advice = analyze_goal(goal)
        print("\n💡 Advice:")
        print(advice)

        display_tasks(tasks)


if __name__ == "__main__":
    main()
