# =========================
#        TASK 1
# =========================

x = float(input("Enter first number: "))
y = float(input("Enter second number: "))
op_choice = input("Choose operation (+,-,*,/): ")

if op_choice == "+":
    print("Result:", x + y)
elif op_choice == "-":
    print("Result:", x - y)
elif op_choice == "*":
    print("Result:", x * y)
elif op_choice == "/":
    if y == 0:
        print("Error: division by zero")
    else:
        print("Result:", x / y)
else:
    print("Wrong operation")


# =========================
#        TASK 2
# =========================

todo = {}

while True:
    cmd = input("\nChoose: add / view / delete / quit → ").lower()

    if cmd == "add":
        task_title = input("Task name: ")
        task_desc = input("Task description: ")
        todo[task_title] = task_desc
        print("Added!")

    elif cmd == "view":
        if not todo:
            print("No tasks yet")
        else:
            for t, d in todo.items():
                print(f"{t} : {d}")

    elif cmd == "delete":
        del_name = input("Task to delete: ")
        if del_name in todo:
            del todo[del_name]
            print("Deleted!")
        else:
            print("Task not found")

    elif cmd == "quit":
        print("Closing task manager...")
        break

    else:
        print("Invalid command")


# =========================
#        TASK 3
# =========================

number_val = int(input("\nEnter number for factorial: "))

res = 1
for step in range(1,
