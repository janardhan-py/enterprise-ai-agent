def initialize_tasks(task_list):
    tasks = []
    for task in task_list :
        tasks.append({
            "task" : task,
            "status" : "todo",
            "priority" : "medium"
        })
    return tasks

def display_tasks(tasks):
    print("\n Task list")

    for idx, task in enumerate(tasks, start=1):
        status = task["status"]
        priority = task["priority"]
        print(f"{idx}.[{status.upper()} | {priority.upper()} | {task['task']}]")


def mark_task_done(tasks, index):
    if 0 <= index < len(tasks):
        tasks[index]["status"] = "done"
