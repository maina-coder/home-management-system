import sqlite3
import msvcrt

# Create/connect to SQLite database
conn = sqlite3.connect("homemanagement.db")
cursor = conn.cursor()

# Create tables if they don't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS resident (
        ID INTEGER PRIMARY KEY AUTOINCREMENT, 
        NAME TEXT NOT NULL,
        AGE INT NOT NULL
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS visitor (
        ID INTEGER PRIMARY KEY AUTOINCREMENT, 
        NAME TEXT NOT NULL,
        PURPOSE TEXT NOT NULL
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS expense (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        EXPENSE_NAME TEXT NOT NULL,
        EXPENSE_VALUE REAL NOT NULL
    )
''')
conn.commit()

# Password input with masking
def input_password(prompt='Enter password: '):
    print(prompt, end='', flush=True)
    password = ''
    while True:
        ch = msvcrt.getch()
        if ch in {b'\r', b'\n'}:
            print()
            break
        elif ch == b'\x08':  # Backspace
            if len(password) > 0:
                password = password[:-1]
                print('\b \b', end='', flush=True)
        else:
            password += ch.decode('utf-8')
            print('*', end='', flush=True)
    return password

# Login
admin = input("Enter username:\n")
password = input_password("Enter password:\n")

# Data lists for in-memory storage (optional)
resident = []
visitor = []
expense = []

# Resident Functions
def addresident():
    print("Welcome!")
    name = input("Enter name of resident:\n")
    try:
        age = int(input("Enter age of the resident:\n"))
        resident_info = {"name": name, "age": age}
        resident.append(resident_info)
        cursor.execute("INSERT INTO resident (NAME, AGE) VALUES (?, ?)", (name, age))
        conn.commit()
        print("Resident added successfully.")
    except ValueError:
        print("Enter a valid age.")

def displayresidents():
    cursor.execute("SELECT NAME, AGE FROM resident")
    rows = cursor.fetchall()
    if not rows:
        print("No residents to display.")
    else:
        for r in rows:
            print("Name:", r[0], ", Age:", r[1])

# Visitor Functions
def addvisitor():
    print("Welcome!")
    name = input("Enter name of visitor:\n")
    purpose = input("Enter purpose of visit:\n")
    visitor_info = {'name': name, 'purpose': purpose}
    visitor.append(visitor_info)
    cursor.execute("INSERT INTO visitor (NAME, PURPOSE) VALUES (?, ?)", (name, purpose))
    conn.commit()
    print("Visitor added successfully.")

def displayvisitors():
    cursor.execute("SELECT NAME, PURPOSE FROM visitor")
    rows = cursor.fetchall()
    if not rows:
        print("No visitors added.")
    else:
        for v in rows:
            print("Name:", v[0], ", Purpose of visit:", v[1])

# Expense Functions
def addexpense():
    expense_name = input("Enter the expense name:\n")
    try:
        value = float(input("Enter expense value in Kshs:\n"))
        expense_info = {'expense name': expense_name, 'expense value': value}
        expense.append(expense_info)
        cursor.execute("INSERT INTO expense (EXPENSE_NAME, EXPENSE_VALUE) VALUES (?, ?)", (expense_name, value))
        conn.commit()
        print("Expense added successfully.")
    except ValueError:
        print("Enter a valid amount.")

def displayexpense():
    cursor.execute("SELECT EXPENSE_NAME, EXPENSE_VALUE FROM expense")
    rows = cursor.fetchall()
    if not rows:
        print("No expenses recorded.")
    else:
        for e in rows:
            print("Expense name:", e[0], ", Expense value:", e[1])

def totalexpense():
    cursor.execute("SELECT SUM(EXPENSE_VALUE) FROM expense")
    total = cursor.fetchone()[0]
    if total is None:
        total = 0
    print("Total expense is Ksh", total)

# Main Program
def main():
    while True:
        print("\n--- Home Management Menu ---")
        print("1. Add resident")
        print("2. Display residents")
        print("3. Add visitor")
        print("4. Display visitors")
        print("5. Add house expense")
        print("6. Display expenses")
        print("7. Total expenses")
        print("8. Exit")

        try:
            choice = int(input("Enter a number to perform an action:\n"))
            if choice == 1:
                addresident()
            elif choice == 2:
                displayresidents()
            elif choice == 3:
                addvisitor()
            elif choice == 4:
                displayvisitors()
            elif choice == 5:
                addexpense()
            elif choice == 6:
                displayexpense()
            elif choice == 7:
                totalexpense()
            elif choice == 8:
                print("Exiting... Goodbye!")
                break
            else:
                print("Invalid option, try again.")
        except ValueError:
            print("Please enter a valid number.")

# Only run the system if credentials are correct
if admin == "mercy" and password == "password":
    main()
else:
    print("Wrong username or password.")
