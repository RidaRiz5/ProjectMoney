from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData
import bcrypt

engine = create_engine("sqlite:///database.db")
metadata = MetaData()

users_table = Table(
    "users", metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String, unique=True),
    Column("password", String)
)
metadata.create_all(engine)

print("✅ Database created successfully!")
