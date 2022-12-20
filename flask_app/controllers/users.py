from flask import Flask, render_template, session, redirect, request
from flask_app import app

from flask_app.models.user import User 
from flask_app.models.coffee import Coffee

from flask import flash

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/register_here")
def register_here():
    return render_template("register.html")

@app.route("/register", methods=["POST"])
def register():
    valid_user = User.create_valid_user(request.form)

    if not valid_user:
        return redirect("/register_here")
    
    session["user_id"] = valid_user.id
    
    return redirect("/dashboard")

@app.route("/login", methods=["POST"])
def login():
        valid_user = User.existing_user(request.form)
    
        if not valid_user:
            return redirect("/")

        user_id = User.get_by_email(request.form["email"])
        session["user_id"] = user_id.id
        return redirect("/dashboard")
    

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        flash("You must be logged in to access the dashboard.")
        return redirect("/")
    
    user = User.get_by_id(session["user_id"])
    coffees = Coffee.get_all()
    
    return render_template("dashboard.html", user=user, coffees=coffees)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")