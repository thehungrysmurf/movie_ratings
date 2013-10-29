from flask import Flask, render_template, redirect, request, flash, session
import model

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
        return render_template("movie_library.html")
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
    model.create_account(email, password, age, gender, zipcode)
    print "Account created successfully!"
    return redirect("/")

if __name__=="__main__":
    app.run(debug=True)