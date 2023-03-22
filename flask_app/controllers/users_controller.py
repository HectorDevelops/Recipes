# only purpose of the controller is to connect to routes 
from flask_app import app
from flask import render_template, redirect, session, request 
from flask_app.models.user_model import User 
from flask_app.models.recipe_model import Recipe 
from flask import flash
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

# ============ Login page - VIEW ============
@app.route("/")
def index():
    return render_template("homepage.html")

# ============ Registering - method - action ============
@app.route("/users/register", methods=['POST'])
def register():
    # This form data gets passed to the to_validate method to ensure it meets the requirements
    result = User.to_validate(request.form)
    # Checks if the usert does NOT meets the validation and if it doesn't it outputs the flash messages
    if not result:
        return redirect("/")
    
    # 1st thing we do is hash the entered password 
    new_password = bcrypt.generate_password_hash(request.form['password'])
    # 2nd thing is to get the data dict ready with the new hashed password to create a user
    user_data = {
        # Unpack everything from request form
        **request.form,
        # Override the following data:
        'password': new_password
    }
    # However, if the user does meet the valdiation, then an user gets created
    # 3rd pass the overwritten data variable to instantiate a new user and RETURNS the id of an user 
    user_id = User.create(user_data)
    # Store user_id of the instance that has logged into the webpage
    session['user_id'] = user_id
    return redirect("/homepage")

@app.route("/homepage")
def home():
    # Creating a ROUTE GUARD - that allows to check if the key is in session, and if not, a user cannot manually visit this page 
    if 'user_id' not in session:
        return redirect("/")
    # Storing the user's id to render to the HTML page
    logged_user = User.get_by_id(session['user_id'])
    all_recipes = Recipe.get_all()
    return render_template("welcome.html", 
                           logged_user = logged_user, 
                           all_recipes=all_recipes)

# ========= This is the log out =========
@app.route('/logout')
def logout():
    # Clears session when logging out
    session.clear()
    return redirect("/")

# ========= This is the log in route - action / post  =========
@app.route("/users/login", methods=['POST'])
def login():
    registered_user = User.get_by_email(request.form['email'])

    # if the email is not in the database, flash the following message
    if not registered_user:
        flash("No history was found in our records!")
        return redirect("/")
    # checking if the HASHED passwords match - if not, flashing this ambiguious message
    if not bcrypt.check_password_hash(registered_user.password, request.form['password']):
        flash("Invalid credentials!")
        return redirect("/")
     # if everything is runnign smooth then the retrieved data's id gets stored in session for rendering usage
    session['user_id'] = registered_user.id
    
    return redirect("/homepage")

# Creating a delete method to provide user option to delete their uploaded recipes
@app.route("/recipes/<int:id>/delete")
def remove(id):
    data = {
        'id' : id
    }
    Recipe.delete(data)
    return redirect("/homepage")