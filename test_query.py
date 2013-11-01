m = session.query(Movie).filter_by(title="Toy Story").one()
u = session.query(User).get(1)

ratings = u.ratings

other_ratings = session.query(Rating).filter_by(movie_id=m.movie_id).all()

other_users = []

for r in other_ratings:    
    other_users.append(r.user)
 
len(other_users) # 452

user_b = other_users[0]


d = {}
common_list = []

for rating in u.ratings:
    d[rating.movie_id] = rating.rating
 
len(d) # 272

for rating in user_b.ratings:
    if d.get(rating.movie_id):
        common_list.append((d[rating.movie_id], rating.rating))
 
len(common_list) # 157


def similarity(user_object_1, user_object_2):
    d = {}
    common_list = []

    for rating in user_object_1.ratings:
        d[rating.movie_id] = rating.rating

    for rating in user_object_2.ratings:
        if d.get(rating.movie_id):
            common_list.append((d[rating.movie_id], rating.rating))

    if common_list:
        return pearson(common_list)
    else:
        return 0.0

