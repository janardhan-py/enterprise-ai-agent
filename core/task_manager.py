PRIORITY_ORDER = {
    "high": 1,
    "medium": 2,
    "low": 3
}



def initialize_tasks(task_list):
    tasks = []
    for task in task_list:
        tasks.append({
            "task": task,
            "status": "todo",
            "priority": "medium"
        })
    return tasks


def display_tasks(tasks):
    print("\n📋 Task List:")
    for idx, task in enumerate(tasks, start=1):
        print(
            f"{idx}. "
            f"[{task['status'].upper()} | {task['priority'].upper()}] "
            f"{task['task']}"
        )


def mark_task_done(tasks, index):
    if 0 <= index < len(tasks):
        tasks[index]["status"] = "done"


def get_next_task(tasks):
    """
    Decide the next best task:
    - Only tasks with status 'todo'
    - Highest priority first
    """
    pending = [t for t in tasks if t["status"] == "todo"]

    if not pending:
        return None

    pending.sort(key=lambda t: PRIORITY_ORDER.get(t["priority"], 2))
    return pending[0]

def update_task_priority(tasks, index, priority):
    if 0 <= index < len(tasks):
        if priority in ["high", "medium", "low"]:
            tasks[index]["priority"] = priority

def execute_task(tasks, task):
    for t in tasks:
        if t == task:
            t['status']= "done"
            return  True
    return False

def count_execution_tasks(tasks):
    return sum(1 for t in tasks if t["status"]== "done")