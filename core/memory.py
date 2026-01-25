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
    if not Memory_File.exists():
        return None
    with open(Memory_File, "r" ) as f :
        return json.load(f)
