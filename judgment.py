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
        return render_template("movie_library.html", user_object=user_object)
    else:
        flash("Login incorrect!")
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

@app.route("/rating/<u_id>")
def view_ratings(u_id):
    user_object = model_session.query(model.User).filter_by(user_id=u_id).first()
    return render_template("movie_library.html", user_object=user_object)

if __name__=="__main__":
    app.run(debug=True)