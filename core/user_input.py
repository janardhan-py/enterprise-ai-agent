

def get_user_details():
    name = input("Enter your name : ")
    goal = input(" Enter your goal : ")
    return name, goal

def ask_user_choice():
    print("\Options")
    print("1. Keep existing goal")
    print("2. update goal")
    print("3. reset goal")

    return input("choose (1/2/3) ").strip()
