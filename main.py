from core.user_input import get_user_details
from core.memory import load_memory , save_memory

memory = load_memory()

if memory:
    print(f"welcome back, {memory['name']}")
    print(f"last Goal", {memory['goal']})

else :
    name , goal = get_user_details()
    save_memory(name , goal)
    print(" Your details have been saved")