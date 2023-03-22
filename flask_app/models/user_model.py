from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash 
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

# Create User class
class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


# ========= Creating a user =========
    @classmethod 
    def create(cls, data):
        # Utilizing this query to insert new users into our database
        query = """
            INSERT INTO users (first_name, last_name, email, password)
            VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
        """
        return connectToMySQL(DATABASE).query_db(query, data)
    
        # Creating a get one method to select a specific user by ID
    @classmethod
    def get_by_id(cls, id):
        data = {
            'id' : id
        }
        query = """
            SELECT * FROM users
            WHERE users.id = %(id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query, data)
        print(results)
        if len(results) < 1:
            return False
        user_instance = cls(results[0])
        return user_instance
    
    # Retrieveing the user by email to authenticate and instantiate the user's email info 
    @classmethod 
    def get_by_email(cls, email):
        data = {
            'email' : email
        }
        query = """
            SELECT * FROM users
            WHERE users.email = %(email)s;
        """
        results = connectToMySQL(DATABASE).query_db(query, data)
        print(results)
        if len(results) < 1:
            return False
        user_instance = cls(results[0])
        return user_instance
        # print(f"=====\n\n{user_instance.email}\n\n======")
            
    # ========= We will be validating =========
    # Staticmethods do not take class or self
    @staticmethod 
    # Data is being grabbed from the request.form (immutable dictionary) the user entered in the register route
    def to_validate(data):
        is_valid = True 
        # Checking each of the form's data being passed to ensure it meets the requirements, otherwise - flash
        if len(data['first_name']) < 2:
            is_valid = False
            flash("Please enter a first name!")
        if len(data['last_name']) < 2:
            is_valid = False
            flash("Please enter a last name!")
        if len(data['email']) < 1:
            is_valid = False
            flash("Please enter a email!")
        # Utlizing this elief statement to ensure that the user is entering a correct email format that follows convention
        elif not EMAIL_REGEX.match(data['email']):
            is_valid = False
            flash("Invalid email address!")
            # This will return false or a user depending if the user is in the database or not
        else:
            lead = User.get_by_email(data['email'])
            if lead:
                is_valid = False
                flash("This email is already in use")

        if len(data['password']) < 1:
            is_valid = False
            flash("Please enter a password!")
            # Password is being checked with the already entered password
        elif not data['password'] == data['confirm_password']:
            is_valid = False
            flash("Ensure the passwords match!!")

        return is_valid 
    