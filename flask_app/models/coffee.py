from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_bcrypt import Bcrypt
from flask_app.models import user
import re

DB = "coffee" 
    
class Coffee:
    def __init__(self, coffee):
        self.id= coffee["id"]
        self.name= coffee["name"]
        self.description= coffee["description"]
        self.date= coffee["date"]
        self.created_at = coffee["created_at"]
        self.updated_at = coffee["updated_at"]
        self.user = None
        
    #create new valid coffee
    @classmethod
    def create_valid_coffee(cls, coffee_dict):
        if not cls.is_valid(coffee_dict):
            return False
        
                
        query = """INSERT INTO coffees (name, description, date, user_id) VALUES (%(name)s, %(description)s, %(date)s, %(user_id)s);"""
        coffee_id = connectToMySQL(DB).query_db(query, coffee_dict)
        coffee = cls.get_by_id(coffee_id)

        return coffee
        
    #getting by id
    @classmethod
    def get_by_id(cls, coffee_id):
        print(f"get coffee by id {coffee_id}")
        data = {"id": coffee_id}
        query = """SELECT coffees.id, coffees.created_at, coffees.updated_at, name, description, date, 
                    users.id as user_id, first_name, last_name, email, address, city, state, zip, users.created_at as uc, users.updated_at as uu
                    FROM coffees
                    JOIN users on users.id = coffees.user_id
                    WHERE coffees.id = %(id)s;"""
        
        result = connectToMySQL(DB).query_db(query,data)
        print("result of query:")
        print(result)
        result = result[0]
        coffee = cls(result)
        
        # convert joined user data into a user object
        coffee.user = user.User(
                {
                    "id": result["user_id"],
                    "first_name": result["first_name"],
                    "last_name": result["last_name"],
                    "email": result["email"],
                    "password": None,
                    "created_at": result["uc"],
                    "updated_at": result["uu"]
                }
            )

        return coffee
    
    
    @classmethod
    def get_all(cls):

        query = """SELECT 
                    coffees.id, coffees.created_at, coffees.updated_at, description, name, date,
                    users.id as user_id, first_name, last_name, email, address, city, state, zip, users.created_at as uc, users.updated_at as uu
                    FROM coffees
                    JOIN users on users.id = coffees.user_id;"""
        coffee_data = connectToMySQL(DB).query_db(query)


        coffees = []

        # Iterate through the list of recipe dictionaries and convert data into object
        for coffee in coffee_data:
            coffee_obj = cls(coffee)

            # convert joined user data into a user object
        coffee_obj.user = user.User(
            {
                "id": coffee["user_id"],
                "first_name": coffee["first_name"],
                "last_name": coffee["last_name"],
                "email": coffee["email"],
                "password": None,
                "created_at": coffee["uc"],
                "updated_at": coffee["uu"]
            }
        )
        coffees.append(coffee_obj)


        return coffees
    
    
    @classmethod
    def update_coffee(cls, coffee_dict, session_id):

        # Authenticate User first
        coffee = cls.get_by_id(coffee_dict["id"])
        if coffee.user.id != session_id:
            flash("You must be the creator to update this coffee.")
            return False

        # Validate the input
        if not cls.is_valid(coffee_dict):
            return False
        
        # Update the data in the database.
        query = """UPDATE coffees
                    SET name = %(name)s, description = %(description)s, date=%(date)s
                    WHERE id = %(id)s;"""
        result = connectToMySQL(DB).query_db(query,coffee_dict)
        coffee = cls.get_by_id(coffee_dict["id"])
        print("****************")
        print(coffee)
        return coffee
    
    @classmethod
    def search(cls, coffee_dict, session_dict):
        coffee = cls.get_by_id(coffee_dict["id"])
        query = "SELECT * FROM coffees WHERE "
        
    
    @classmethod
    def delete_coffee_by_id(cls, coffee_id):

        data = {"id": coffee_id}
        query = "DELETE from coffees WHERE id = %(id)s;"
        connectToMySQL(DB).query_db(query,data)

        return coffee_id
    
    @staticmethod
    def is_valid(coffee_dict):
        valid = True
        flash_string = " field is required and must be at least 3 characters."
        if len(coffee_dict["name"]) < 3:
            flash("name " + flash_string)
            valid = False
        if len(coffee_dict["description"]) < 3:
            flash("Description " + flash_string)
            valid = False

        if len(coffee_dict["date"]) <= 0:
            flash("Date is required.")
            valid = False


        return valid