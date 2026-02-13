import logging
logging.getLogger("sentence_transformers").setLevel(logging.ERROR)
logging.getLogger("transformers").setLevel(logging.ERROR)
logging.getLogger("huggingface_hub").setLevel(logging.ERROR)


from core.logger import setup_logger
from core.user_input import get_user_details, ask_user_choice
from core.memory import load_memory, save_full_state, reset_memory
from core.rules import analyze_goal
from core.planner import generate_tasks
from core.task_manager import (
    initialize_tasks,
    display_tasks,
    mark_task_done,
    get_next_task,
    update_task_priority,
    execute_task,
)
from core.llm_reasoner import (
    build_context,
    llm_reason,
    validate_llm_output,
)
from core.vector_memory import VectorMemory


MAX_EXECUTIONS_PER_RUN = 2


def run_llm_pipeline(name, goal, tasks, vector_memory):
    """
    Handles LLM reasoning with validation and fallback.
    Keeps main() clean and readable.
    """
    context = build_context(name, goal, tasks, vector_memory)
    llm_data = llm_reason(context)

    if validate_llm_output(llm_data):
        advice = llm_data["advice"]
        raw_tasks = [t["task"] for t in llm_data["tasks"]]
    else:
        logging.warning("Invalid LLM output. Falling back to rule-based logic.")
        advice = analyze_goal(goal)
        raw_tasks = generate_tasks(goal)

    return advice, raw_tasks


def handle_task_updates(name, goal, tasks):
    """
    Handles priority updates, marking done, and execution logic.
    """
    display_tasks(tasks)

    next_task = get_next_task(tasks)

    if next_task:
        print("\n➡️ Recommended Next Task:")
        print(f"- {next_task['task']} (priority: {next_task['priority']})")
    else:
        print("\n🎉 All tasks are completed!")

    # ---- Update Priority ----
    priority_choice = input(
        "\nEnter task number to change PRIORITY (or press Enter to skip): "
    ).strip()

    if priority_choice.isdigit():
        task_index = int(priority_choice) - 1
        new_priority = input(
            "Set priority (high / medium / low): "
        ).strip().lower()

        update_task_priority(tasks, task_index, new_priority)
        save_full_state(name, goal, tasks)
        print("✅ Task priority updated")

    # ---- Mark Done ----
    done_choice = input(
        "\nEnter task number to mark DONE (or press Enter to skip): "
    ).strip()

    if done_choice.isdigit():
        mark_task_done(tasks, int(done_choice) - 1)
        save_full_state(name, goal, tasks)
        print("✅ Task marked as DONE")

    # ---- Execution Guardrails ----
    executed_count = sum(1 for t in tasks if t["status"] == "done")

    if executed_count >= MAX_EXECUTIONS_PER_RUN:
        print("\n🛑 Execution limit reached for this session.")
        print("Restart the application to continue.")
        return

    execute_choice = input(
        "\nExecute recommended task now? (y/n): "
    ).strip().lower()

    if execute_choice == "y" and next_task:
        success = execute_task(tasks, next_task)

        if success:
            save_full_state(name, goal, tasks)
            print("⚙️ Task executed and marked as DONE")
        else:
            print("❌ Failed to execute task")


def main():
    setup_logger()
    logging.info("Application started")

    vector_memory = VectorMemory()
    memory = load_memory()

    # ==================================================
    # EXISTING USER
    # ==================================================
    if memory:
        name = memory.get("name", "User")
        goal = memory.get("goal", "")
        tasks = memory.get("tasks", [])

        print(f"\n👋 Welcome back, {name}")
        print("\n🎯 Current Goal:")
        print(goal)

        advice, raw_tasks = run_llm_pipeline(name, goal, tasks, vector_memory)

        print("\n💡 Advice:")
        print(advice)

        if not tasks:
            tasks = initialize_tasks(raw_tasks)
            save_full_state(name, goal, tasks)

        handle_task_updates(name, goal, tasks)

        # ---- User Control ----
        choice = ask_user_choice()

        if choice == "2":
            print("\nUpdate your goal:")
            new_name, new_goal = get_user_details()

            advice, raw_tasks = run_llm_pipeline(new_name, new_goal, [])
            tasks = initialize_tasks(raw_tasks)

            save_full_state(new_name, new_goal, tasks)
            vector_memory.store(new_goal)

            print("✅ Goal updated successfully")

        elif choice == "3":
            reset_memory()
            print("🗑️ Memory reset successfully")

        else:
            print("➡️ Continuing with current plan")

    # ==================================================
    # FIRST RUN
    # ==================================================
    else:
        logging.info("First run detected")

        name, goal = get_user_details()

        advice, raw_tasks = run_llm_pipeline(name, goal, [])
        tasks = initialize_tasks(raw_tasks)

        save_full_state(name, goal, tasks)
        vector_memory.store(goal)

        print(f"\n👋 Welcome, {name}")
        print("\n🎯 Your Goal:")
        print(goal)

        print("\n💡 Advice:")
        print(advice)

        display_tasks(tasks)

        next_task = get_next_task(tasks)
        if next_task:
            print("\n➡️ Recommended Next Task:")
            print(f"- {next_task['task']} (priority: {next_task['priority']})")


if __name__ == "__main__":
    main()
