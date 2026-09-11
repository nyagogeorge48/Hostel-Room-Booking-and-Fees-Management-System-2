
import json
import os

FILE = "hostel_data.txt"

hostels = {
    "Block A": {"A101": [4, []], "A102": [4, []], "A103": [2, []]},
    "Block B": {"B101": [4, []], "B102": [4, []], "B103": [2, []]},
    "Block C": {"C101": [3, []], "C102": [3, []], "C103": [2, []]}
}

students = {}


def save():
    try:
        with open(FILE, "w") as f:
            json.dump({"hostels": hostels, "students": students}, f)
        print("Records saved.")
    except OSError:
        print("Could not save records.")


def load():
    global hostels, students

    if not os.path.exists(FILE):
        return

    try:
        with open(FILE, "r") as f:
            data = json.load(f)

        hostels = data["hostels"]
        students = data["students"]

    except (OSError, json.JSONDecodeError, KeyError):
        print("Saved file is damaged.")
        students = {}


def overview():
    print("\n===== OCCUPANCY OVERVIEW =====")

    for block, rooms in hostels.items():
        used = sum(len(r[1]) for r in rooms.values())
        total = sum(r[0] for r in rooms.values())
        print(f"{block}: {used}/{total} occupied")


def register():
    print("\n===== STUDENT REGISTRATION =====")

    reg = input("Registration number: ").strip()
    name = input("Student name: ").strip()

    if not reg or not name or reg in students:
        print("Invalid or duplicate student details.")
        return

    print("Blocks:", ", ".join(hostels))
    block = input("Block: ").strip()

    if block not in hostels:
        print("Invalid block.")
        return

    print("Rooms:", ", ".join(hostels[block]))
    room = input("Room: ").strip()

    if room not in hostels[block]:
        print("Invalid room.")
        return

    r = hostels[block][room]

    if len(r[1]) >= r[0]:
        print("Room is full.")
        return

    try:
        fee = float(input("Total fee: "))

        if fee < 0:
            raise ValueError

    except ValueError:
        print("Invalid fee.")
        return

    students[reg] = {
        "name": name,
        "block": block,
        "room": room,
        "fee": fee,
        "payments": []
    }

    r[1].append(reg)

    print("Student registered successfully.")


def payment():
    print("\n===== FEE PAYMENT =====")

    reg = input("Registration number: ").strip()

    if reg not in students:
        print("Student not found.")
        return

    s = students[reg]
    paid = sum(s["payments"])
    balance = s["fee"] - paid

    print(f"Student: {s['name']}")
    print(f"Outstanding balance: {balance:.2f}")

    if balance <= 0:
        print("Fees are fully paid.")
        return

    try:
        amount = float(input("Payment amount: "))

        if amount <= 0 or amount > balance:
            print("Invalid payment amount.")
            return

    except ValueError:
        print("Enter a valid amount.")
        return

    s["payments"].append(amount)

    new_balance = s["fee"] - sum(s["payments"])

    print(f"New balance: {new_balance:.2f}")


def search():
    key = input("\nEnter name or registration number: ").lower()
    found = False

    for reg, s in students.items():

        if key == reg.lower() or key in s["name"].lower():

            paid = sum(s["payments"])
            balance = s["fee"] - paid

            print(f"\nName: {s['name']}")
            print(f"Registration: {reg}")
            print(f"Room: {s['block']} {s['room']}")
            print(f"Fee: {s['fee']:.2f}")
            print(f"Paid: {paid:.2f}")
            print(f"Balance: {balance:.2f}")

            found = True

    if not found:
        print("Student not found.")


def report():
    print("\n===== OCCUPANCY REPORT =====")

    for block, rooms in hostels.items():

        print(f"\n{block}")

        for room, r in rooms.items():
            print(f"{room}: {len(r[1])}/{r[0]} occupied")


def defaulters():
    try:
        limit = float(input("\nEnter balance threshold: "))

    except ValueError:
        print("Invalid amount.")
        return

    print("\n===== FEE DEFAULTERS =====")

    found = False

    for reg, s in students.items():

        balance = s["fee"] - sum(s["payments"])

        if balance > limit:
            print(
                f"{s['name']} | {reg} | "
                f"Balance: {balance:.2f}"
            )
            found = True

    if not found:
        print("No defaulters found.")


def main():

    load()
    overview()

    while True:

        print("""
===== HOSTEL MANAGEMENT SYSTEM =====
1. Register student
2. Record payment
3. Search student
4. Occupancy report
5. Fee defaulters
6. Save and exit
""")

        choice = input("Choose: ").strip()

        if choice == "1":
            register()

        elif choice == "2":
            payment()

        elif choice == "3":
            search()

        elif choice == "4":
            report()

        elif choice == "5":
            defaulters()

        elif choice == "6":
            save()
            print("System closed.")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
