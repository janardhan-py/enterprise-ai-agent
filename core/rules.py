
def analyze_goal(goal: str) -> str:
    goal = goal.lower()

    if "ai" in goal or "machine learning" in goal:
        return "You should focus on Python, data structures, and ML basics."

    if "germany" in goal:
        return "Focus on German language, system design, and EU-compliant AI."

    if "job" in goal or "career" in goal:
        return "Build real projects, maintain GitHub, and practice interviews."

    return "Break your goal into smaller tasks and work consistently."

