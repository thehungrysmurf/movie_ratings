from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, scoped_session

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

import correlation

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

    def similarity(user_object_1, user_object_2):
        d = {}
        common_list = []

        for rating in user_object_1.ratings:
            d[rating.movie_id] = rating.rating

        for rating in user_object_2.ratings:
            if d.get(rating.movie_id):
                common_list.append((d[rating.movie_id], rating.rating))

        if common_list:
            return correlation.pearson(common_list)
        else:
            return 0.0

    def predict_rating(self, movie):
        ratings = self.ratings # ratings object for the user that we want prediction for
        other_ratings = movie.movie_ratings # all rating objects for the movie object
        
        similarities = [(self.similarity(r.user), r) for r in other_ratings] 
        # list of tuples of [(similarity, rating object)]
        similarities.sort(reverse=True) # sorted list starting with [(highest sim, rating object)]
        
        numerator = 0
        for s,r in similarities:
            if s>0:
                numerator += r.rating * s

        denominator = 0
        for s in similarities:
            if s>0:
                denominator += s[0]

        return numerator / denominator


class Movie(Base):
    __tablename__ = "movies"

    movie_id = Column(Integer, primary_key = True)
    title = Column(String(64), nullable = True)
    release_date = Column(DateTime, nullable = True)
    imdb_url = Column(String(100), nullable = True)

class Rating(Base):
    __tablename__ = "ratings"

    rating_id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    movie_id = Column(Integer, ForeignKey('movies.movie_id'))
    rating = Column(Integer, nullable = True)

    user = relationship("User", backref=backref("ratings", order_by=user_id))
    movie = relationship("Movie", backref=backref("movie_ratings", order_by=movie_id))


### End class declarations

engine = create_engine("sqlite:///ratings.db", echo=False)
session = scoped_session(sessionmaker(bind=engine, autocommit = False, autoflush = False))

Base = declarative_base()
Base.query = session.query_property()

def authenticate(email, password):
    user_query = session.query(User).filter_by(email = email).first()
    if user_query:
        if password == user_query.password:
            return True
        else:
            return False
    else:
        return False

def create_account(email, password, age, gender, zipcode):
    user = User(email=email, password=password, age=age, zip_code=zipcode, gender=gender)
    session.add(user)
    session.commit()

def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()
