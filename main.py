import time

def main():
    print("Welcome to the elite 101 chatbot")

    name = input("What is your name? ")
    age = input(f"Nice to meet you, {name}! What is your age? ")

    print(f"Wow! You are {age} years old. That's awesome!")
    print("I am a chatbot and I am here to help you with anything you need.")

    time.sleep(1)
    print("")
    time.sleep(1)

    print("Please choose from the following options: ")
    print("1. Tell me a joke")
    print("2. Tell me a fact")
    print("3. Tell me a quote")
    print("4. Exit")

    while True:
        choice = input("Enter the number of your choice: ")
        if choice == "1":
            print("Why did the scarecrow win an award? Because he was outstanding in his field!")
        elif choice == "2":
            print("The shortest war in history lasted only 38 minutes!")
        elif choice == "3":
            print("The only way to do great work is to love what you do. - Steve Jobs")
        elif choice == "4":
            print("Goodbye! Have a great day!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
