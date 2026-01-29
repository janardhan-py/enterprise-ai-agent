from core.user_input import get_user_details , ask_user_choice
from core.memory import load_memory , save_memory, reset_memory
import logging
from core.logger import setup_logger

setup_logger()

logging.info("Application started ")

memory = load_memory()

if memory:
    logging.info("Existing memory found")
    print(f"welcome back, {memory['name']}")
    print(f"last Goal", {memory['goal']})

    choice = ask_user_choice()

    if choice == '2':
        _, new_goal = get_user_details()
        save_memory(memory["name"], new_goal)
        logging.info("user goal updated")
        print("Goal updated successfully.")
    
    elif choice == '3':
        reset_memory()
        logging.info("Memory reset by user")
        print("memory reset successfully.")

    else:
        logging.info("user continue  with exixting goal")
        print("continuw with existing goal ")

else :
    logging.info("No memory found, asking user input")
    name , goal = get_user_details()
    save_memory(name , goal)
    print(" Your details have been saved")