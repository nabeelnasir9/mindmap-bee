from app.db.session import db


def init_db():
    # Create indices for faster queries (e.g., unique email in user collection)
    db.users.create_index("email", unique=True)
    db.notes.create_index("user_id")
