import logging

from core.logger import setup_logger
from core.user_input import get_user_details, ask_user_choice
from core.memory import load_memory, save_full_state, reset_memory
from core.rules import analyze_goal
from core.planner import generate_tasks
from core.task_manager import initialize_tasks,  display_tasks  , mark_task_done, get_next_task, update_task_priority, execute_task
  



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

        # ----- Intelligence Layer -----
        advice = analyze_goal(active_goal)
        print("\n💡 Advice:")
        print(advice)

        # ----- Task Planning Layer -----
        if not tasks:
            raw_tasks = generate_tasks(active_goal)
            tasks = initialize_tasks(raw_tasks)
            save_full_state(name, active_goal, tasks)

        display_tasks(tasks)

        # ----- Agent Decision -----
        next_task = get_next_task(tasks)
        if next_task:
            print("\n➡️ Next Best Task:")
            print(f"- {next_task['task']} (priority: {next_task['priority']})")
        else:
            print("\n🎉 All tasks are completed!")

        # ----- Mark Task Done -----
        done_choice = input(
            "\nEnter task number to mark DONE (or press Enter to skip): "
        ).strip()

        if done_choice.isdigit():
            mark_task_done(tasks, int(done_choice) - 1)
            save_full_state(name, active_goal, tasks)
            print("✅ Task marked as DONE")

        execute_choice = input(
            "\n Execute next task now? (y/n)"
        ).strip().lower()

        if execute_choice == "y" and next_task:
            success =execute_task(tasks, next_task)

            if success:
                save_full_state(name, active_goal, tasks)
                print("⚙️ Task executed and marked as DONE")
            else:
                print("❌ Failed to execute task")

        # ----- Update Task Priority -----
        priority_choice = input(
            "\nEnter task number to change PRIORITY (or press Enter to skip): "
        ).strip()

        if priority_choice.isdigit():
            task_index = int(priority_choice) - 1
            new_priority = input(
                "Set priority (high / medium / low): "
            ).strip().lower()

            update_task_priority(tasks, task_index, new_priority)
            save_full_state(name, active_goal, tasks)
            print("✅ Task priority updated")

        # ----- User Control -----
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
            logging.info("User kept existing plan")
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

        next_task = get_next_task(tasks)
        if next_task:
            print("\n➡️ Next Best Task:")
            print(f"- {next_task['task']} (priority: {next_task['priority']})")


if __name__ == "__main__":
    main()
