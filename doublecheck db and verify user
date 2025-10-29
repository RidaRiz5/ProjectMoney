# database.py
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, select
import bcrypt
import os

# Ensure database exists in working directory
DB_FILE = "database.db"
DB_PATH = f"sqlite:///{os.path.abspath(DB_FILE)}"

engine = create_engine(DB_PATH, connect_args={"check_same_thread": False})
metadata = MetaData()

users_table = Table(
    "users", metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String, unique=True),
    Column("password", String)
)

# Create the table if it doesn't exist
metadata.create_all(engine)

# Create new user
def create_user(username, password):
    with engine.begin() as conn:
        # Check if username exists
        existing = conn.execute(
            select(users_table.c.username).where(users_table.c.username == username)
        ).fetchone()
        if existing:
            return False  # username already taken

        # Hash the password (ensure encoding)
        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        conn.execute(users_table.insert().values(username=username, password=hashed))
    return True


# Verify user credentials
def verify_user(username, password):
    with engine.begin() as conn:
        result = conn.execute(
            select(users_table.c.password).where(users_table.c.username == username)
        ).fetchone()
        if not result:
            return False
        stored = result[0]
        return bcrypt.checkpw(password.encode("utf-8"), stored.encode("utf-8"))
