import json
from pathlib import Path

Memory_File = Path("data/memory.json")

def save_memory(name, goal):
    data = {
        "name" : name,
        "goal" : goal
        }
    with open(Memory_File,"w")as f :
        json.dump(data, f, indent=4)

        
def load_memory():
    try :
        if not Memory_File.exists():
            return None
        with open(Memory_File, "r" ) as f :
            return json.load(f)
    except json.JSONDecodeError:
        return None
    
def reset_memory():
    if Memory_File.exists():
        Memory_File.unlink()

def save_full_state(name, goal, tasks):
    data = {
        "name" : name,
        "goal" : goal,
        "tasks" : tasks
    }
    Memory_File.parent.mkdir(exist_ok = True)
    with open(Memory_File,"w") as f:
        json.dump(data, f , indent = 4)