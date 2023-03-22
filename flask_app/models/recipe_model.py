from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash 
from flask_app.models import user_model 

class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.under_thirty = data['under_thirty']
        self.date = data['date']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']


    # ============= Creating =============
    @classmethod
    def create(self, data):
        query = """
                INSERT INTO recipes (name, description, instructions, date, under_thirty, user_id)
                VALUES (%(name)s, %(description)s, %(instructions)s, %(date)s, %(under_thirty)s, %(user_id)s);
        """
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod 
    def get_all(cls):
        query = """
                SELECT * FROM recipes 
                JOIN users
                ON recipes.user_id = users.id;
            """
        results = connectToMySQL(DATABASE).query_db(query)
        print(f"=========\n\n{results}\n\n=========")
        list_of_recipes = []
        for row in results:
            # Instantianting each recipe 
            this_recipe = cls(row)
            # Creating user for the recipe 
            user_data = {
                **row, 
                'id': row['users.id'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at']
            }
            #  Creating an instance of the user
            this_user = user_model.User(user_data)
            # Adding a new attribute to the recipe 
                # for each row, a recipe is created and a user [this_user] is placed in the chef variable 
            this_recipe.chef = this_user
            list_of_recipes.append(this_recipe)
        return list_of_recipes

    # This will get each recipe by the id to render 
    @classmethod 
    def get_by_id(cls, id):
        # Preparing the data dictionary for the query dictionary 
        data = {
            'id': id
        }
        query = """
            SELECT * FROM recipes
            JOIN users
            ON recipes.user_id = users.id
            WHERE recipes.id = %(id)s;
        """

        results = connectToMySQL(DATABASE).query_db(query, data)
        print(results)
        # Instantiate the dictionary list 
        this_recipe = cls(results[0])
        # Creating the user for the recipe 
        row = results[0]
        user_info = {
            **results[0],
            'id' :row['users.id'],
            'created_at' :row['users.created_at'],
            'updated_at' :row['users.updated_at']
        }
        the_user = user_model.User(user_info)
        this_recipe.chef = the_user
        return this_recipe


    # Update method
    @classmethod 
    def update (cls, data):
        query = """
            UPDATE recipes 
            SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, under_thirty = %(under_thirty)s, date = %(date)s
            WHERE id = %(id)s; 
        """
        return connectToMySQL(DATABASE).query_db(query, data)


    # this is the validator for our recipes 
    @staticmethod 
    def validate(data):
        is_valid = True 

        if len(data['name']) < 3:
            is_valid = False 
            flash("Name should not be blank")
            
        if len(data['description']) < 3:
            is_valid = False 
            flash("Description should not be blank")

        if len(data['instructions']) < 3:
            is_valid = False 
            flash("Instructions should not be blank")

        if len(data['date']) < 1:
            is_valid = False 
            flash("Date is required")
        
        if 'under_thirty' not in data:
            is_valid = False 
            flash(" Cooking time is required")

        return is_valid
    
    @classmethod
    def delete(cls, data):
        query = """
            DELETE FROM recipes 
            WHERE id = %(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query, data)
