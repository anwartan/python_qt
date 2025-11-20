from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
engine = create_engine('sqlite:///passwords.db',echo=False)
sessionlocal = sessionmaker(bind=engine)