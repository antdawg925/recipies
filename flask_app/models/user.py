
from inspect import classify_class_attrs
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from flask_app.models.recipe import Recipe 

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

# USER NAME _____________________________________________________________________________________________
    @classmethod
    def get_name(cls,data):
        query = "SELECT first_name FROM users LEFT JOIN recipes ON users.id = recipes.user_id WHERE new_recipes_db.users.id = %(id)s;"
        result = connectToMySQL('new_recipes_db').query_db(query,data)
        print('***********************', result)
        return cls(result[0]) 

# GET USER INFO_________________________________________________________________________________________________
    @classmethod
    def get_one(cls,data):
        print('getting individual user')
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL('new_recipes_db').query_db(query,data)
        print('***********************', result)
        print("got user")
        return cls(result[0])

# SAVE USER_________________________________________________________________________________________________
    @classmethod
    def save(cls, data):
        query = "INSERT INTO users ( first_name, last_name, email, password) " \
        "VALUES (%(first_name)s , %(last_name)s , %(email)s , %(password)s );"
        result = connectToMySQL('new_recipes_db').query_db(query,data)
        print('***********************', result)
        print('saved the new user to database')
        return result


# FIND USER BY EMAIL__________________________________________________________________________________________
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL("new_recipes_db").query_db(query,data)
        print('***********************', result)
        if not result:
            flash("not enough information provided")
            return False
        return cls(result[0])


# VALIDATE USER REG INFO______________________________________________________________________________________
    @staticmethod
    def validate_info(user):
        is_valid = True
        if len(user['first_name']) < 3:
            flash("First name must be at least 3 characters.")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Last name must be at least 3 characters.")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email!")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters.")
            is_valid = False
        if len(user['confirm']) < 3:
            flash("Confirm password must be at least 3 characters.")
            is_valid = False
        if user['confirm'] != user['password']:
            flash("Password and confirm password do not match.")
            is_valid = False
        print('valid entered info send to bcrypt')
        return is_valid

# VALIDATE LOGIN INFO________________________________________________________________________________________
    @staticmethod
    def validate_login( user ):
        print('validating login info')
        is_valid = True
        if len(user['email']) < 3:
            flash("Email must be at least 3 characters.")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email/password!")
            is_valid = False
            print('passes regex step')
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters.")
            is_valid = False
        return is_valid

