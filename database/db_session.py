from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
engine = create_engine('sqlite:///password.db', echo=True)
sessionlocal = sessionmaker(bind=engine)