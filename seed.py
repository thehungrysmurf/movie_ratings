import model
import csv
import datetime

def load_users(session):
    with open("seed_data/u.user") as u:
        reader = csv.reader(u, delimiter='|')
        for line in reader:
            user = model.User(user_id=line[0], age=line[1], zip_code=line[4], gender=line[2])
            session.add(user)
    session.commit()

def load_movies(session):
    with open("seed_data/u.item") as m:
        reader = csv.reader(m, delimiter='|')
        for line in reader:
            if line[2] == '':
                movie_date = None
            else:
                movie_date = datetime.datetime.strptime(line[2], "%d-%b-%Y")
            movie_title = line[1].decode("latin-1").split(" (")
            movie = model.Movie(movie_id = line[0], title=movie_title[0], release_date=movie_date, imdb_url=line[4])
            session.add(movie)
    session.commit()

def load_ratings(session):
    with open("seed_data/u.data") as r:
        reader = csv.reader(r, delimiter='\t')
        for line in reader:
            rating = model.Rating(user_id=line[0], movie_id=line[1], rating=line[2])
            session.add(rating)
    session.commit()

def main(session):
    # You'll call each of the load_* functions with the session as an argument
    #load_users(session)
    load_movies(session)
    #load_ratings(session)

if __name__ == "__main__":
    s= model.connect()
    main(s)
