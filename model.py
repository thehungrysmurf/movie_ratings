from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker

ENGINE = None
Session = None

Base = declarative_base()

### Class declarations go here

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key = True)
    gender = Column(String(10), nullable = True)
    email = Column(String(64), nullable = True)
    password = Column(String(64), nullable = True)
    age = Column(Integer, nullable = True)
    zip_code = Column(String(15), nullable = True)

class Movie(Base):
    __tablename__ = "movies"

    movie_id = Column(Integer, primary_key = True)
    title = Column(String(64), nullable = True)
    release_date = Column(DateTime, nullable = True)
    imdb_url = Column(String(100), nullable = True)

class Rating(Base):
    __tablename__ = "ratings"

    rating_id = Column(Integer, primary_key = True)
    user_id = Column(Integer, nullable = True)
    movie_id = Column(Integer, nullable = True)
    rating = Column(Integer, nullable = True)

### End class declarations

def connect():
    global ENGINE
    global Session

    ENGINE = create_engine("sqlite:///ratings.db", echo = True)
    Session = sessionmaker(bind=ENGINE)

    return Session()

def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()
