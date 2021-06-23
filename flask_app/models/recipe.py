from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.login import Login

class Recipe():

    def __init__(self, data):
        self.id = data['id']
        self.recipe_name = data['recipe_name']
        self.description = data['recipe_description']
        self.instructions = data['recipe_instructions']
        self.date_created = data['date_created']
        self.under_30 = data['under_30']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None

    @classmethod
    def get_all_recipes(cls):
        query = 'SELECT* FROM recipes JOIN users ON users.id = recipes.creator_id;'

        connection = connectToMySQL('recipes')
        results = connection.query_db(query)

        recipes = []

        for result in results:
            recipe = cls(result)
            user_data = {
                "id": result['users.id'],
                "first_name": result['first_name'],
                "last_name": result['last_name'],
                "email": result['email'],
                "password": result['password'],
                "created_at": result['users.created_at'],
                "updated_at": result['users.updated_at']
            }
            recipe.creator = Login(user_data)
            recipes.append(recipe)

        return recipes

    @classmethod
    def new_recipe(cls, data):
        query = 'INSERT INTO recipes (recipe_name, recipe_description, recipe_instructions, date_created, under_30, creator_id) VALUES (%(recipe_name)s, %(recipe_description)s, %(recipe_instructions)s, %(date_created)s, %(under_30)s, %(creator_id)s);'

        connection = connectToMySQL('recipes')
        return connection.query_db(query, data)

    @classmethod
    def get_recipe_by_id(cls, data):
        query = 'SELECT* FROM recipes JOIN users ON users.id = recipes.creator_id WHERE recipes.id = %(id)s;'

        connection = connectToMySQL('recipes')
        results = connection.query_db(query, data)

        if len(results) == 0:
            print("No recipe by that ID")
            return False

        else:
            result = results[0]
            recipe = cls(result)
            user_data = {
                "id": result['users.id'],
                "first_name": result['first_name'],
                "last_name": result['last_name'],
                "email": result['email'],
                "password": result['password'],
                "created_at": result['users.created_at'],
                "updated_at": result['users.updated_at']
            }
            recipe.creator = Login(user_data)
            return recipe

    @classmethod
    def update_recipe(cls, data):
        query = 'UPDATE recipes SET recipe_name=%(recipe_name)s, recipe_description=%(recipe_description)s, recipe_instructions=%(recipe_instructions)s WHERE id=%(recipe_id)s'

        connection = connectToMySQL('recipes')
        connection.query_db(query, data)

    @classmethod
    def delete_recipe(cls, data):
        query = 'DELETE FROM recipes WHERE id = %(id)s'

        connection = connectToMySQL('recipes')
        connection.query_db(query, data)

    @staticmethod
    def validate_recipe(data):
        is_valid = True

        if len(data['recipe_name']) < 3:
            is_valid = False
            flash("Recipe name must be at least 3 characters")

        if len(data['recipe_description']) < 3:
            is_valid = False
            flash("Recipe description must be at least 3 characters")

        if len(data['recipe_instructions']) < 3:
            is_valid = False
            flash("Recipe instructions must be at least 3 characters")

        if data['date_created'] == '':
            is_valid = False
            flash("Please choose a date when you made this")

        return is_valid