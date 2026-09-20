from cs50 import SQL
from werkzeug.security import generate_password_hash

db = SQL("sqlite:///parkwise.db")

# Define initial residents: (username, temporary_password, house_no)
initial_residents = [
    ("c21", "resident123", "c21"),
    ("c22", "resident123", "c22"),
    ("ab28", "resident123", "ab28"),
    ("ab09", "resident123", "ab09"),
]
# Using Loop for Insering data in table
for username, password, aprt_no in initial_residents:
    hashed_pw = generate_password_hash(password, method="scrypt", salt_length=16)
    try:
        db.execute(
            "INSERT INTO resident (username, hash, aprt_no) VALUES (?, ?, ?)",
            username,
            hashed_pw,
            aprt_no,
        )
        # Printing if insertaion was correct or not
        print(f"Added {username} (Apartment {aprt_no})")
    except Exception as e:
        print(f"Skipped {username} (might already exist)")
