from flask import Flask, render_template, redirect, request, flash, session
import model

from model import session as model_session

app = Flask(__name__)
app.secret_key = "blahblahblah"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/", methods=["POST"])
def process_login():
    email = request.form.get("email")
    password = request.form.get("password")
    if model.authenticate(email, password):
        user_object = model_session.query(model.User).filter_by(email=email).first()
        session['id'] = user_object.user_id
        return render_template("movie_library.html", user_object=user_object)
    else:
        flash("Login incorrect!")
        return redirect("/")

@app.route("/clear")
def clear_session():
    session.clear()
    return redirect("/")


@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/register", methods=["POST"])
def create_account():
    email = request.form.get("email")
    password = request.form.get("password")
    age = request.form.get("age")
    gender = request.form.get("gender")
    zipcode = request.form.get("zipcode")

    user = model.User(email=email, password=password, age=age, zip_code=zipcode, gender=gender)
    model_session.add(user)
    model_session.commit()

    print "Account created successfully!"
    return redirect("/")

@app.route("/users")
def view_users():
    all_users = model_session.query(model.User).all() 
    return render_template("view_users.html", users=all_users)

@app.route("/movies")
def view_movies():
    user_id = session.get('id', None)
    all_movies = model_session.query(model.Movie).all()
    user_object = model_session.query(model.User).filter_by(user_id=user_id).first()
    return render_template("view_movies.html", movies=all_movies, user_id=user_id, user_object=user_object)

# put ids of movies that have been rated in a dictionary as keys (if ids are not in the dictionary, then they haven't been rated)
# remember to fix the release date to only display year

@app.route("/rate/<movie_id>")
def display_rating_form(movie_id):
    movie_object = model_session.query(model.Movie).filter_by(movie_id=movie_id).first()
    return render_template("rate_movie.html", movie_object=movie_object)

@app.route("/rate/<movie_id>", methods=["POST"])
def submit_rating(movie_id):
    rating = request.form.get("rating")
    print "Rating: ", rating
    new_table_rating = model.Rating(movie_id=movie_id, rating=rating, user_id=session['id'])
    model_session.add(new_table_rating)
    model_session.commit()
    print "Rating added successfully!"
    return redirect("/movies")

if __name__=="__main__":
    app.run(debug=True)