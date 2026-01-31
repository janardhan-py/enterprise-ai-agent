import logging

from core.logger import setup_logger
from core.user_input import get_user_details, ask_user_choice
from core.memory import load_memory, save_memory, reset_memory
from core.rules import analyze_goal
from core.planner import generate_tasks


def main():
    setup_logger()
    logging.info("Application started")

    memory = load_memory()

    # -----------------------------
    # CASE 1: Existing memory found
    # -----------------------------
    if memory:
        name = memory.get("name", "User")
        active_goal = memory.get("goal", "")

        print(f"\n👋 Welcome back, {name}")

        print("\n📌 Current Goal:")
        print(active_goal)

        # Intelligence layer
        advice = analyze_goal(active_goal)
        print("\n💡 Advice:")
        print(advice)

        # Planning layer
        tasks = generate_tasks(active_goal)
        print("\n📝 Suggested Task Plan:")
        for idx, task in enumerate(tasks, start=1):
            print(f"{idx}. {task}")

        # User control
        choice = ask_user_choice()

        if choice == "2":
            print("\nUpdate your details:")
            new_name, new_goal = get_user_details()
            save_memory(new_name, new_goal)
            logging.info("User updated name and goal")
            print("✅ Details updated successfully.")

        elif choice == "3":
            reset_memory()
            logging.info("User reset memory")
            print("🗑️ Memory reset successfully.")

        else:
            logging.info("User kept existing goal")
            print("➡️ Continuing with existing goal.")

    # -----------------------------
    # CASE 2: First run (no memory)
    # -----------------------------
    else:
        logging.info("No memory found. First run detected.")

        name, goal = get_user_details()
        save_memory(name, goal)

        print(f"\n👋 Welcome, {name}")
        print("\n📌 Your Goal:")
        print(goal)

        advice = analyze_goal(goal)
        print("\n💡 Advice:")
        print(advice)

        tasks = generate_tasks(goal)
        print("\n📝 Suggested Task Plan:")
        for idx, task in enumerate(tasks, start=1):
            print(f"{idx}. {task}")


if __name__ == "__main__":
    main()
