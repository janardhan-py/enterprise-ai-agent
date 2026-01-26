from core.user_input import get_user_details , ask_user_choice
from core.memory import load_memory , save_memory, reset_memory

memory = load_memory()

if memory:
    print(f"welcome back, {memory['name']}")
    print(f"last Goal", {memory['goal']})

    choice = ask_user_choice()

    if choice == '2':
        _, new_goal = get_user_details()
        save_memory(memory["name"], new_goal)
        print("Goal updated successfully.")
    
    elif choice == '3':
        reset_memory()
        print("memory reset successfully.")

    else:
        print("continuw with existing goal ")

else :
    name , goal = get_user_details()
    save_memory(name , goal)
    print(" Your details have been saved")