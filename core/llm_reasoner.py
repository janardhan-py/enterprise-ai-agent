from core.vector_memory import VectorMemory


SYSTEM_PROMPT = """
You are an AI planning assistant.

Rules:
- Output MUST be valid JSON
- Do NOT include explanations outside JSON
- Tasks must be actionable
- Priority must be one of: high, medium, low
- Do NOT repeat completed tasks
"""


def build_context(name, goal, tasks):
    vector_memory = VectorMemory()

    completed = [t["task"] for t in tasks if t["status"] == "done"]
    pending = [t["task"] for t in tasks if t["status"] == "todo"]

    related_memory = vector_memory.retrieve(goal, top_k=1)

    return {
        "user": name,
        "goal": goal,
        "completed_tasks": completed,
        "pending_tasks": pending,
        "related_memory": related_memory,
    }


def llm_reason(context: dict) -> dict:
    """
    LLM reasoning function.
    For now this is a stub (mock).
    Later this will call OpenAI / Azure OpenAI.
    """

    # ---- MOCK RESPONSE (SAFE PLACEHOLDER) ----
    return {
        "advice": (
            "Based on your progress, focus next on high-impact tasks "
            "that improve employability in Germany."
        ),
        "tasks": [
            {
                "task": "Prepare a German-style resume (CV)",
                "priority": "high",
            },
            {
                "task": "Practice German interview questions",
                "priority": "medium",
            },
        ],
    }


def validate_llm_output(data: dict) -> bool:
    """
    Validate LLM output before using it.
    """
    if not isinstance(data, dict):
        return False

    if "advice" not in data or "tasks" not in data:
        return False

    if not isinstance(data["tasks"], list):
        return False

    for task in data["tasks"]:
        if (
            "task" not in task
            or "priority" not in task
            or task["priority"] not in ["high", "medium", "low"]
        ):
            return False

    return True
