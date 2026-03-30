from connect import connect
import csv


# Create table
def create_table():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS phonebook (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        phone VARCHAR(20),
        UNIQUE(name, phone)
    )
    """)

    conn.commit()
    cur.close()
    conn.close()


# Add contact manually
def add_contact(name, phone):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO phonebook (name, phone)
        VALUES (%s, %s)
        ON CONFLICT (name, phone) DO NOTHING
    """, (name, phone))

    conn.commit()
    cur.close()
    conn.close()


# Input contact from console
def add_contact_from_input():
    name = input("Enter name: ")
    phone = input("Enter phone: ")
    add_contact(name, phone)


# Import from CSV (NO duplicates)
def import_from_csv(filename):
    conn = connect()
    cur = conn.cursor()

    with open(filename, newline='') as file:
        reader = csv.reader(file)
        next(reader, None)

        for row in reader:
            if len(row) != 2:
                continue

            name, phone = row

            cur.execute("""
                INSERT INTO phonebook (name, phone)
                VALUES (%s, %s)
                ON CONFLICT (name, phone) DO NOTHING
            """, (name, phone))

    conn.commit()
    cur.close()
    conn.close()


# Show all contacts
def get_all():
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM phonebook")
    rows = cur.fetchall()

    if not rows:
        print("No data")
    else:
        for row in rows:
            print(f"ID: {row[0]} | Name: {row[1]} | Phone: {row[2]}")

    cur.close()
    conn.close()


# Update phone
def update_contact(name, new_phone):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "UPDATE phonebook SET phone = %s WHERE name = %s",
        (new_phone, name)
    )

    conn.commit()
    cur.close()
    conn.close()


# Search by name
def search_by_name(name):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM phonebook WHERE name ILIKE %s",
        ('%' + name + '%',)
    )

    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


# Delete contact
def delete_contact(value):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM phonebook WHERE name = %s OR phone = %s",
        (value, value)
    )

    conn.commit()
    cur.close()
    conn.close()


# MAIN MENU
if __name__ == "__main__":
    create_table()

    while True:
        print("\n1 - Import CSV")
        print("2 - Add contact")
        print("3 - Show all")
        print("4 - Update phone")
        print("5 - Search by name")
        print("6 - Delete contact")
        print("0 - Exit")

        choice = input("Choose: ")

        if choice == "1":
            import_from_csv("contacts.csv")

        elif choice == "2":
            add_contact_from_input()

        elif choice == "3":
            get_all()

        elif choice == "4":
            name = input("Name: ")
            phone = input("New phone: ")
            update_contact(name, phone)

        elif choice == "5":
            name = input("Search name: ")
            search_by_name(name)

        elif choice == "6":
            val = input("Enter name or phone: ")
            delete_contact(val)

        elif choice == "0":
            break

        else:
            print("Invalid choice")