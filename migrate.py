from database.db_session import engine
from database.entity.base import Base
from database.entity.account import Account
print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully.")