from database.db_session import engine
from database.entity.base import Base
from database.entity.Account import Account
from database.entity.egg import Egg
print("creating database tables...")
Base.metadata.create_all(bind=engine)
print("table created successfully.")
