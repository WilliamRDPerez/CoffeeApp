from flask import render_template, session, redirect, request, url_for
from flask_app import app

from flask_app.models.user import User 
from flask_app.models.coffee import Coffee
import os


from flask import flash


#create new order
@app.route("/create") 
def create():
    if "user_id" not in session:
        flash("You must be logged in to create.")
        return redirect("/")
    
    user = User.get_by_id(session["user_id"])
    #need to add get all 
    return render_template("neworder.html")


@app.route("/create/new", methods=["POST"])
def create_coffee():
    valid_coffee = Coffee.create_valid_coffee(request.form)
    if valid_coffee:
        return redirect(f'/coffees/{valid_coffee.id}')
    return redirect('/create')


#view entry by id
# Details page
@app.route("/coffees/<int:coffee_id>")
def coffee_detail(coffee_id):
    user = User.get_by_id(session["user_id"])
    coffee = Coffee.get_by_id(coffee_id)
    return render_template("yourorder.html", user=user, coffee=coffee)
#may need to add similar to recipe=recipe after user=user



#Edit order page
@app.route("/coffees/edit/<int:coffee_id>")
def coffee_edit_page(coffee_id):
    if "user_id" not in session:
        flash("You must be logged in to create.")
        return redirect("/")
    
    coffee = Coffee.get_by_id(coffee_id)
    return render_template("edit.html", coffee=coffee)

@app.route("/coffees/edit/<int:coffee_id>", methods=["POST"])
def update_coffee(coffee_id):

    valid_coffee = Coffee.update_coffee(request.form, session["user_id"])

    if not valid_coffee:
        return redirect(f"/coffees/edit/{coffee_id}")
        
    return redirect(f"/coffees/{coffee_id}")


#Profile Page
@app.route("/profile")
def profile():
    if "user_id" not in session:
        flash("You must be logged in to access the dashboard.")
        return redirect("/")
    
    user = User.get_by_id(session["user_id"])
    #coffees = Coffee.get_all()
    
    return render_template("account.html", user=user) #coffees=coffees)

@app.route("/updateprofile/<int:id>", methods=["POST"])
def updateprofile(id):
    if not User.validate_update(request.form):
        return redirect ('/profile')

    User.update(request.form)
    return redirect('/dashboard')



@app.route("/coffees/delete/<int:coffee_id>")
def delete_by_id(coffee_id):
    Coffee.delete_coffee_by_id(coffee_id)
    return redirect("/dashboard")