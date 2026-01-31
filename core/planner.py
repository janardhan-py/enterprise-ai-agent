
def generate_tasks(goal : str ) -> list :
    goal = goal.lower()
    tasks = []

    if "ai" in goal :
        tasks.extend([
            "Learn python fundamentals",
            "Study basic machine learining concepts",
            "Build small AI related projects",
            "Create a github porfolio"
        ])
    
    if "germany" in goal :
        tasks.extend([
            "learn German langage level upto B1/B2",
            "prepare a german-style resume (CV)",
            "research AI job market in Germany",
            "Apply to relevent companies"
        ])
    if "job" in goal and "career" in goal :
        tasks.extend([
            "Improve problem solving skills",
            "Practice interview questions",
            "Network in Linkedin",
            "Apply consistency every week"
        ])
    if not tasks:
        tasks.append("Break your tasks into smaller weekly goals")

    return tasks
