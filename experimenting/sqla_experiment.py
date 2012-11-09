from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

# This is a Base object that is required for SQLalchemy to work
Base = declarative_base()

# Create the database and set it up
Engine = None
Session = None
# Base.metadata.create_all(engine) --- Type this if you need to initialize the database

#############################
#############################
#############################

class User(Base):

    __tablename__ = "Users"

    id = Column(Integer, primary_key=True)
    email = Column(String(64))
    password = Column(String(64))
    age = Column(Integer)
    zipcode = Column(String(15))

    def __init__(self, email, password, age, zipcode):
        self.email = email
        self.password = password
        self.age = age
        self.zipcode = zipcode

#############################
#############################
#############################


def connect():
    global Engine
    global Session

    Engine = create_engine("sqlite:///ratings.db", echo=True)
    Session = sessionmaker(bind=Engine)

    return Session()

session = connect()

def main():

    pass


if __name__ == "__main__":
    main()










