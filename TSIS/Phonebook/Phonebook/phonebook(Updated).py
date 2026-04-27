from connect import connect
import csv
import os
import json
base_dir = os.path.dirname(__file__)
file_path = os.path.join(base_dir, "contacts.csv")


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


# Extend table
def extend_table():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        ALTER TABLE phonebook
        ADD COLUMN IF NOT EXISTS email VARCHAR(100),
        ADD COLUMN IF NOT EXISTS birthday DATE;
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS groups (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50) UNIQUE NOT NULL
        );
    """)

    cur.execute("""
        ALTER TABLE phonebook
        ADD COLUMN IF NOT EXISTS group_id INTEGER REFERENCES groups(id);
    """)

    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phones (
            id SERIAL PRIMARY KEY,
            contact_id INTEGER REFERENCES phonebook(id) ON DELETE CASCADE,
            phone VARCHAR(20) NOT NULL,
            type VARCHAR(10) CHECK (type IN ('home', 'work', 'mobile')),
            UNIQUE(contact_id, phone)
        );
    """)

    conn.commit()
    cur.close()
    conn.close()


# Add contact
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


# Add full contact
def add_full_contact(name, phone, email, birthday, group=None, phone_type="mobile"):
    conn = connect()
    cur = conn.cursor()

    try:
        # 1. Creating 
        cur.execute("""
            INSERT INTO phonebook (name, phone, email, birthday)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """, (name, phone, email, birthday))

        contact_id = cur.fetchone()[0]

        # 2.Adding into phones
        cur.execute("""
            INSERT INTO phones (contact_id, phone, type)
            VALUES (%s, %s, %s)
            ON CONFLICT (contact_id, phone) DO NOTHING
        """, (contact_id, phone, phone_type))

        # Adding group if exists
        if group:
            cur.execute("""
                INSERT INTO groups(name)
                VALUES (%s)
                ON CONFLICT (name) DO NOTHING
            """, (group,))

            cur.execute("SELECT id FROM groups WHERE name = %s", (group,))
            group_id = cur.fetchone()[0]

            cur.execute("""
                UPDATE phonebook
                SET group_id = %s
                WHERE id = %s
            """, (group_id, contact_id))

        conn.commit()
        print(f" Contact added: {name}")

        return contact_id

    except Exception as e:
        print(" Error:", e)

    finally:
        cur.close()
        conn.close()


# Add phone
def add_phone(contact_id, phone, type_):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO phones (contact_id, phone, type)
        VALUES (%s, %s, %s)
        ON CONFLICT (contact_id, phone) DO NOTHING
    """, (contact_id, phone, type_))

    conn.commit()
    cur.close()
    conn.close()


# Add group
def add_group(name):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO groups (name)
        VALUES (%s)
        ON CONFLICT (name) DO NOTHING
    """, (name,))

    conn.commit()
    cur.close()
    conn.close()


# Assign group
def assign_group(contact_id, group_id):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        UPDATE phonebook
        SET group_id = %s
        WHERE id = %s
    """, (group_id, contact_id))

    conn.commit()
    cur.close()
    conn.close()


# Input contact
def add_contact_from_input():
    name = input("Enter name: ")
    phone = input("Enter phone: ")
    add_contact(name, phone)


# Import simple CSV
def import_from_csv(filename):
    conn = connect()
    cur = conn.cursor()

    with open(filename, newline='', encoding='utf-8') as file:
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


# Import extended CSV with group and phone type
def import_full_csv(filename):
    conn = connect()
    cur = conn.cursor()

    try:
        with open(filename, newline='', encoding='utf-8-sig') as file:

            # Detect delimiter
            sample = file.read(1024)
            file.seek(0)
            delimiter = ',' if sample.count(',') >= sample.count(';') else ';'

            reader = csv.DictReader(file, delimiter=delimiter)

            if not reader.fieldnames:
                print("CSV header not found")
                return

            for row in reader:
                try:
                    # Normalize keys and values
                    clean_row = {
                        (k.strip().lower() if k else ""): (v.strip() if v else "")
                        for k, v in row.items()
                    }

                    name = clean_row.get("name", "")
                    phone = clean_row.get("phone", "")
                    email = clean_row.get("email", "")
                    birthday = clean_row.get("birthday", "")
                    group = clean_row.get("group", "")
                    ptype = clean_row.get("type", "mobile")

                    if not name or not phone:
                        continue

                    # Insert or update contact
                    cur.execute("""
                        INSERT INTO phonebook (name, phone, email, birthday)
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT (name, phone)
                        DO UPDATE SET
                            email = EXCLUDED.email,
                            birthday = EXCLUDED.birthday
                        RETURNING id
                    """, (name, phone, email, birthday))

                    contact_id = cur.fetchone()[0]

                    # Assign group
                    if group:
                        cur.execute("""
                            INSERT INTO groups(name)
                            VALUES (%s)
                            ON CONFLICT (name) DO NOTHING
                        """, (group,))

                        cur.execute("SELECT id FROM groups WHERE name = %s", (group,))
                        group_id = cur.fetchone()[0]

                        cur.execute("""
                            UPDATE phonebook
                            SET group_id = %s
                            WHERE id = %s
                        """, (group_id, contact_id))

                    # Insert phone
                    cur.execute("""
                        INSERT INTO phones (contact_id, phone, type)
                        VALUES (%s, %s, %s)
                        ON CONFLICT (contact_id, phone) DO NOTHING
                    """, (contact_id, phone, ptype))

                except Exception:
                    continue

        conn.commit()

    finally:
        cur.close()
        conn.close()

# Show all (simple)
def get_all():
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM phonebook")
    rows = cur.fetchall()

    if not rows:
        print("  (no contacts found)")
    for row in rows:
        print(row)

    cur.close()
    conn.close()


#Getting full contacts
def get_full_contacts():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT 
            p.id,
            p.name,
            p.phone        AS main_phone,
            p.email,
            p.birthday,
            g.name         AS group_name,
            ph.phone       AS extra_phone,
            ph.type        AS phone_type
        FROM phonebook p
        LEFT JOIN groups g  ON p.group_id = g.id
        LEFT JOIN phones ph ON p.id = ph.contact_id
        ORDER BY p.id
    """)

    rows = cur.fetchall()
    cur.close()
    conn.close()

    if not rows:
        print("  (no contacts found — try importing first)")
        return

    # Group phones per contact
    contacts = {}
    for row in rows:
        cid, name, main_phone, email, birthday, group_name, extra_phone, phone_type = row

        if cid not in contacts:
            contacts[cid] = {
                "id": cid,
                "name": name,
                "main_phone": main_phone,
                "email": email,
                "birthday": birthday,
                "group": group_name,
                "phones": []
            }

        if extra_phone:
            contacts[cid]["phones"].append(f"{extra_phone} ({phone_type})")

    print(f"\n{'─'*60}")
    for c in contacts.values():
        phones_str = ", ".join(c["phones"]) if c["phones"] else "—"
        print(f"ID:       {c['id']}")
        print(f"Name:     {c['name']}")
        print(f"Phone:    {c['main_phone'] or '—'}")
        print(f"Email:    {c['email'] or '—'}")
        print(f"Birthday: {c['birthday'] or '—'}")
        print(f"Group:    {c['group'] or '—'}")
        print(f"Phones:   {phones_str}")
        print(f"{'─'*60}")


# Update
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


# Search
def search_by_name(name):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM phonebook WHERE name ILIKE %s",
        ('%' + name + '%',)
    )

    rows = cur.fetchall()
    if not rows:
        print("  (not found)")
    for row in rows:
        print(row)

    cur.close()
    conn.close()


# Delete
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

#Export from Json
def export_to_json(filename="contacts.json"):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT 
            p.id,
            p.name,
            p.email,
            p.birthday,
            g.name AS group_name,
            ph.phone,
            ph.type
        FROM phonebook p
        LEFT JOIN groups g ON p.group_id = g.id
        LEFT JOIN phones ph ON p.id = ph.contact_id
        ORDER BY p.id
    """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    contacts = {}

    for row in rows:
        cid, name, email, birthday, group_name, phone, phone_type = row

        if cid not in contacts:
            contacts[cid] = {
                "name": name,
                "email": email,
                "birthday": str(birthday) if birthday else None,
                "group": group_name,
                "phones": []
            }

        if phone:
            contacts[cid]["phones"].append({
                "number": phone,
                "type": phone_type
            })

    # Convering to string
    result = list(contacts.values())

    # Dumping
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

    print(f" Exported to {filename}")

def import_from_json(filename="contacts.json"):
    conn = connect()
    cur = conn.cursor()

    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)

        for contact in data:
            try:
                name = contact.get("name", "").strip()
                email = contact.get("email", "").strip()
                birthday = contact.get("birthday")
                phones = contact.get("phones", [])
                group = contact.get("group")

                if not name:
                    print(f"[!] Skipping invalid contact: {contact}")
                    continue

                # Check if conctact exists
                cur.execute("SELECT id FROM phonebook WHERE name = %s", (name,))
                existing = cur.fetchone()

                if existing:
                    choice = input(f"Contact '{name}' exists. (s)kip / (o)verwrite? ").lower()

                    if choice == "s":
                        print(f"  ⏭ Skipped: {name}")
                        continue

                    elif choice == "o":
                        contact_id = existing[0]

                        # Updating
                        cur.execute("""
                            UPDATE phonebook
                            SET email = %s,
                                birthday = %s
                            WHERE id = %s
                        """, (email, birthday, contact_id))

                    #Deleting old phones
                        cur.execute("DELETE FROM phones WHERE contact_id = %s", (contact_id,))

                    else:
                        print("  [!] Invalid choice, skipping")
                        continue

                else:
                #New contact
                    cur.execute("""
                        INSERT INTO phonebook (name, email, birthday)
                        VALUES (%s, %s, %s)
                        RETURNING id
                    """, (name, email, birthday))

                    contact_id = cur.fetchone()[0]

               #Checking groups
                if group:
                    cur.execute("""
                        INSERT INTO groups(name)
                        VALUES (%s)
                        ON CONFLICT (name) DO NOTHING
                    """, (group,))

                    cur.execute("SELECT id FROM groups WHERE name = %s", (group,))
                    group_id = cur.fetchone()[0]

                    cur.execute("""
                        UPDATE phonebook
                        SET group_id = %s
                        WHERE id = %s
                    """, (group_id, contact_id))

                # 📱 телефоны
                for ph in phones:
                    number = ph.get("number")
                    ptype = ph.get("type", "mobile")

                    if number:
                        cur.execute("""
                            INSERT INTO phones (contact_id, phone, type)
                            VALUES (%s, %s, %s)
                            ON CONFLICT (contact_id, phone) DO NOTHING
                        """, (contact_id, number, ptype))

                print(f"  [+] Imported: {name}")

            except Exception as e:
                print(f"  [ERROR] Contact failed: {contact} -> {e}")

        conn.commit()
        print(" JSON IMPORT DONE")

    except Exception as e:
        print(" File error:", e)

    finally:
        cur.close()
        conn.close()
    #Filter by group
def filter_by_group(group_name):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT p.name, p.email, p.phone, g.name
        FROM phonebook p
        JOIN groups g ON p.group_id = g.id
        WHERE g.name ILIKE %s
    """, ('%' + group_name + '%',))

    rows = cur.fetchall()

    if not rows:
        print("  (no contacts in this group)")
    else:
        print("\n--- GROUP RESULTS ---")
        for r in rows:
            print(f"Name: {r[0]} | Email: {r[1]} | Phone: {r[2]} | Group: {r[3]}")

    cur.close()
    conn.close()       
        
def search_by_email(query):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT name, email, phone
        FROM phonebook
        WHERE email ILIKE %s
    """, ('%' + query + '%',))

    rows = cur.fetchall()

    if not rows:
        print("  (not found)")
    else:
        print("\n--- RESULTS ---")
        for r in rows:
            print(f"Name: {r[0]} | Email: {r[1]} | Phone: {r[2]}")

    cur.close()
    conn.close()
    
def sort_contacts(sort_by="name"):
    conn = connect()
    cur = conn.cursor()

    allowed = {
        "name": "p.name",
        "birthday": "p.birthday",
        "id": "p.id"
    }

    if sort_by not in allowed:
        print(" Invalid sort field")
        return

    order = allowed[sort_by]

    cur.execute(f"""
        SELECT 
            p.id,
            p.name,
            p.phone,
            p.email,
            p.birthday,
            g.name
        FROM phonebook p
        LEFT JOIN groups g ON p.group_id = g.id
        ORDER BY {order}
    """)

    rows = cur.fetchall()

    if not rows:
        print("  (no contacts)")
    else:
        print(f"\n--- SORTED BY {sort_by.upper()} ---")
        for r in rows:
            print(f"ID: {r[0]} | Name: {r[1]} | Phone: {r[2]} | Email: {r[3]} | Birthday: {r[4]} | Group: {r[5]}")

    cur.close()
    conn.close()
    
# MAIN MENU
if __name__ == "__main__":
    create_table()
    extend_table()

    while True:
        print("\n1  - Import CSV")
        print("2  - Add contact")
        print("3  - Show all")
        print("4  - Update phone")
        print("5  - Search by name")
        print("6  - Delete contact")
        print("7  - Add full contact")
        print("8  - Add phone")
        print("9  - Add group")
        print("10 - Show full info")
        print("11 - Import full CSV")
        print("12 - Export to JSON")
        print("13 - Import JSON")
        print("14 - Search by email")
        print("15 - Filter by group")
        print("16 - Sort contacts")
        print("0  - Exit")

        choice = input("Choose: ")

        if choice == "1":
            import_from_csv(file_path)

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

        elif choice == "7":
         name = input("Name: ")
         phone = input("Phone: ")
         email = input("Email: ")
         birthday = input("Birthday (YYYY-MM-DD): ")
         group = input("Group (optional): ")
         ptype = input("Phone type (home/work/mobile): ")

         add_full_contact(name, phone, email, birthday, group, ptype)

        elif choice == "8":
            cid = int(input("Contact ID: "))
            phone = input("Phone: ")
            type_ = input("Type (home/work/mobile): ")
            add_phone(cid, phone, type_)

        elif choice == "9":
            group_name = input("Group name: ")
            add_group(group_name)

        elif choice == "10":
            get_full_contacts()

        elif choice == "11":
            full_path = os.path.join(base_dir, "contacts_full.csv")
            import_full_csv(full_path)
        elif choice == "12":
            export_to_json()
        elif choice == "13":
            import_from_json()
        elif choice == "14":
             q = input("Enter email (e.g. gmail): ")
             search_by_email(q)
        elif choice == "15":
            g = input("Enter group name: ")
            filter_by_group(g)
        elif choice == "16":
            print("Sort by: name / birthday / id")
            s = input("Enter: ").lower()
            sort_contacts(s)
        elif choice == "0":
            break

        else:
            print("Invalid choice")