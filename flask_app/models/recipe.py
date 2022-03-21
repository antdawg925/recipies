from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user


class Recipe:

    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.min30 = data['min30']
        self.description = data['description']
        self.instructions = data['instructions']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

# Recipe Info INCLUDING USER NAME_____________________________________________________________________________________________
    @classmethod
    def one_recipe(cls,data):
        query = "SELECT * FROM users LEFT JOIN recipes ON users.id = recipes.user_id WHERE new_recipes_db.users.id = %(id)s;"
        result = connectToMySQL('new_recipes_db').query_db(query,data)
        print('***********************', result)
        return cls(result[0]) 

# SAVE USER_________________________________________________________________________________________________
    @classmethod
    def save(cls, data):
        query = "INSERT INTO recipes ( name, min30, description, instructions, user_id) VALUES (%(name)s , %(min30)s , %(description)s , %(instructions)s, %(user_id)s);"
        print('saved the new user to database')
        return connectToMySQL('new_recipes_db').query_db(query , data) 


# UPDATE THE RECIPE____________________________________________________________________________________
    @classmethod
    def update(cls,data): 
        query= "UPDATE new_recipes_db.recipes SET name =  %(name)s, min30 = %(min30)s, description=%(description)s, instructions=%(instructions)s  WHERE id = %(id)s;"
        print('just updated the pie')
        return connectToMySQL('new_recipes_db').query_db(query, data)

# DELETE A RECIPE_________________________________________________________________________________
    @classmethod
    def delete(cls,data):
        print('deleted listing')
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL('new_recipes_db').query_db(query , data)

# GET RECIPE_________________________________________________________________________________________________
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        result = connectToMySQL('new_recipes_db').query_db(query,data)
        print('***********************', result)
        print("got recipe")
        return cls(result[0])

# GET ALL RECIPES____________________________________________________________________________________
    @classmethod
    def get_all(cls):
        print('retrieving all pies info')
        query = "SELECT * FROM recipes LEFT JOIN users ON users.id = recipes.user_id" 
        results = connectToMySQL('new_recipes_db').query_db(query)
        recipes = []
        for recipe in results:
            recipes.append( cls(recipe) )
        return recipes


# GET ALL USERS AND RECIPES____________________________________________________________________________________
    @classmethod
    def get_all_users_and_recipes(cls):
        print('retrieving all pies info')
        query = "SELECT * FROM recipes LEFT JOIN users ON users.id = recipes.user_id" 
        results = connectToMySQL('new_recipes_db').query_db(query)
        print(results)

        if not results:
            return[]
        all_recipes=[]

        for dict in results:
            recipe_actual=cls(dict)
            data = {
                'id' :dict['users.id'],
                'created_at' :dict['users.created_at'],
                'updated_at' :dict['users.updated_at'],
                'first_name' :dict['first_name'],
                'last_name' :dict['last_name'],
                'email' :dict['email'],
                'password' :dict['password'],
                
            }

            recipe_actual.user = user.User(data)
            all_recipes.append(recipe_actual )
        return all_recipes
