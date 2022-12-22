from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_bcrypt import Bcrypt
from flask_app.models import user
import re

DB = "coffee" 
    
class Coffee:
    def __init__(self, coffee):
        self.id = coffee["idw"]
        self.size = coffee["size"]
        self.carry_out = coffee["carry_out"]
        self.temp = coffee["temp"]
        self.quantity = coffee["quantity"]
        self.coffee = coffee["coffee"]
        self.latte = coffee["latte"]
        self.americano = coffee["americano"]
        self.cappuccino = coffee["cappuccino"]
        self.caramel = coffee["caramel"]
        self.espresso = coffee["espresso"]
        self.created_at = coffee["created_at"]
        self.updated_at = coffee["updated_at"]
        self.user = None
        
    #create new valid coffee
    @classmethod
    def create_valid_coffee(cls, coffee_dict):
        if not cls.is_valid(coffee_dict):
            return False
        
                
        query = """INSERT INTO coffees (size, carry_out, temp, quantity, coffee, latte, americano, cappuccino, caramel, espresso, user_id) VALUES (%(size)s, %(carry_out)s, %(temp)s, %(quantity)s, %(coffee)s, %(latte)s, %(americano)s, %(cappucino)s, %(caramel)s, %(espresso)s, %(user_id)s);"""
        coffee_id = connectToMySQL(DB).query_db(query, coffee_dict)
        coffee = cls.get_by_id(coffee_id)

        return coffee
        
    #getting by id
    @classmethod
    def get_by_id(cls, coffee_id):
        print(f"get coffee by id {coffee_id}")
        data = {"id": coffee_id}
        query = """SELECT coffees.id, coffees.created_at, coffees.updated_at, carry_out, size, carry_out, temp, quantity, coffee, latte, americano, cappuccino, caramel, espresso,
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
                    "first_name" : result["first_name"],
                    "last_name" : result["last_name"],
                    "email" : result["email"],
                    "address" : result["address"],
                    "city" : result["city"],
                    "state" : result["state"],
                    "zip" : result["zip"],
                    "password": None,
                    "created_at": result["uc"],
                    "updated_at": result["uu"]
                }
            )

        return coffee
    
    
    @classmethod
    def get_all(cls):

        query = """SELECT coffees.id, coffees.created_at, coffees.updated_at, carry_out, size, carry_out, temp, quantity, coffee, latte, americano, cappuccino, caramel, espresso,
                    user_id as users_id, first_name, last_name, email, address, city, state, zip, users.created_at as uc, users.updated_at as uu
                    FROM coffees
                    JOIN users on users.users_id = coffees.user_id;"""
        coffee_data = connectToMySQL(DB).query_db(query)


        coffees = []

        # Iterate through the list of recipe dictionaries and convert data into object
        for coffee in coffee_data:
            coffee_obj = cls(coffee)

            # convert joined user data into a user object
        coffee_obj.user = user.User(
                {
                    "id": coffee["user_id"],
                    "first_name" : coffee["first_name"],
                    "last_name" : coffee["last_name"],
                    "email" : coffee["email"],
                    "address" : coffee["address"],
                    "city" : coffee["city"],
                    "state" : coffee["state"],
                    "zip" : coffee["zip"],
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
                    SET 
                    size = %(size)s, carry_out = %(carry_out)s, temp = %(temp)s, quantity = %(quantity)s, coffee - %(coffee)s, latte = %(latte)s, americano = %(americano)s, cappucino = %(cappucino)s, caramel = %(caramel)s, espresso = %(espresso)s
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
        if 'quantity' not in coffee_dict:
            flash("Give me a number.")
            is_valid = False
        if 'size' not in coffee_dict:
            flash("Give me a size.")
            is_valid = False
        if 'temp' not in coffee_dict:
            flash("Give me a number.")
            is_valid = False

        return valid