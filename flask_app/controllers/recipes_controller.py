# only purpose of the controller is to connect to routes 
from flask_app import app
from flask import render_template, redirect, session, request 
from flask_app.models.user_model import User 
from flask_app.models.recipe_model import Recipe 
from flask import flash


# This page will render the new recipe site 
@app.route('/recipes/new')
def new_recipe():
    return render_template ("new_recipe.html")

# This page will create our submitted form data and re-direct to homepage
@app.route('/recipes/create', methods=['POST'])
def create_recipe():
    # print(f"====\n\n {request.form}\n\n =======")
    # Invoking the validate method to validate the submitted data 
    recipe_data_submitted = Recipe.validate(request.form)
    # If the user successfully fills out the form, then re-direct to homepage
    if not recipe_data_submitted:
        return redirect("/recipes/new")
    # Invoking this recipe_creation to create the submitted data into our database 
    recipe_creation = Recipe.create(request.form)
    
    return redirect("/homepage")

@app.route("/recipes/<int:id>")
def show_one_recipe(id):
    # Bringing logged_user to display the user's information
    logged_user = User.get_by_id(session['user_id'])
    this_recipe = Recipe.get_by_id(id)
    return render_template("view_recipe.html",
                           this_recipe = this_recipe,
                           logged_user = logged_user)

# This route will help update the recipe's information
@app.route("/recipes/<int:id>/edit")
def edit_recipe(id):
    this_recipe = Recipe.get_by_id(id)
    return render_template("recipe_edit.html", 
                           this_recipe=this_recipe)

# This route will serve to update our data in our database
@app.route("/recipes/update", methods=['POST'])
def updating():
    # print(f"====\n\n {request.form}\n\n =======")
    # Using our validations to ensure the users meet requirements before updating
    if not Recipe.validate(request.form):
        return redirect(f"/recipes/{request.form['id']}/edit")
    
    Recipe.update(request.form)
    return redirect("/homepage")

