def llm_reason(goal: str) -> dict:
     """
    LLM is used only for reasoning.
    It must return structured JSON.
    """
     # This is a placeholder (real API later)
     return{
          "advice" : "Focus on German language, resume tailoring, and targeted applications.",

          "tasks" : [
               {"task" : "Prepare German-style resume (CV)", "priority": "high"},
               {"task": "Improve German to B1/B2 level", "priority": "medium"},
               {"task": "Apply to AI roles in Germany", "priority": "medium"}
          ]
     }

def validate_llm_output(data : dict) -> bool:
    if "advice" not in data or "tasks" not in data:
          return False
     
    for t in data["tasks"]:
          if "task" not in t or "priority" not in t:
               return False
    return True 