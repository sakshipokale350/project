import sqlite3

def create_db():
    # Connect to SQLite database (or create it if it doesn't exist)
    con = sqlite3.connect(database="rms.db")
    cur = con.cursor()

    # === Table for course details ===
    cur.execute("""
        CREATE TABLE IF NOT EXISTS course(
            cid INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            duration TEXT,
            charges TEXT,
            description TEXT
        )
    """)
    con.commit()

    # === Table for student details ===
    cur.execute("""
        CREATE TABLE IF NOT EXISTS student(
            roll INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            gender TEXT,
            dob TEXT,
            contact TEXT,
            admission TEXT,
            course TEXT,
            state TEXT,
            city TEXT,
            pin TEXT,
            address TEXT
        )
    """)
    con.commit()

    # === Table for result records ===
    cur.execute("""
        CREATE TABLE IF NOT EXISTS result(
            rid INTEGER PRIMARY KEY AUTOINCREMENT,
            roll TEXT,
            name TEXT,
            course TEXT,
            marks_ob TEXT,
            full_marks TEXT,
            per TEXT
        )
    """)
    con.commit()

    # === Table for login/registration details ===
    cur.execute("""
        CREATE TABLE IF NOT EXISTS data(
            eid INTEGER PRIMARY KEY AUTOINCREMENT,
            F_NAME TEXT,
            L_NAME TEXT,
            CONTACT TEXT,
            EMAIL TEXT UNIQUE,
            QUESTION TEXT,
            ANSWER TEXT,
            PASSWORD TEXT
        )
    """)
    con.commit()

    # Close the connection
    con.close()

# Call the function to create the database and tables
create_db()
