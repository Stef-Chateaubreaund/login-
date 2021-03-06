from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
import re

class User:
    def __init__(self,data):
        self.id = data["id"]
        self.first_name = data ["first_name"]
        self.last_name = data ["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
    
    @classmethod
    def save(cls,data):
        query = "INSERT INTO registration (first_name, last_name, email, password) VALUES (%(first_name)s,%(last_name)s, %(email)s, %(password)s)"
        return connectToMySQL("login_schema").query_db(query,data)

    @staticmethod
    def reg_valid(user_data):
        is_valid = True
        query="SELECT * FROM registration WHERE email = %(email)s"
        results = connectToMySQL("login_schema").query_db(query,user_data)
        print(results)
        email_reg = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if len(results) >= 1: 
            flash("Email exists") 
            is_valid = False
        if len(user_data["email"]) < 1:
            flash("please fill your name")
            is_valid = False
        if len(user_data["first_name"]) < 2:
            flash("please fill your first name")
            is_valid = False
        if len(user_data["last_name"]) < 2:
            flash("please fill your last name")
            is_valid = False
        if not email_reg.match(user_data['email']):
            flash("invalid data")
            is_valid = False
        if len(user_data["password"]) < 8:
            flash("confirm your password")
            is_valid = False
        if user_data["confirm_pass"] != user_data["password"]:
            flash("Confirm password again")
            is_valid = False
        if User.get_by_email(user_data):
            flash("Email is already registered, please enter a unique email address")
            is_valid = False
        

        return is_valid

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM registration WHERE email = %(email)s"
        user_db = connectToMySQL("login_schema").query_db(query,data)
        print()

        if len(user_db) < 1:  #-- how to fix this error?
            return False  #-- if len keeps showing up as a error
        
        return cls(user_db[0])