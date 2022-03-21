from distutils.command import config
from flask import Flask, render_template, request, redirect, session, flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_app.models.recipe import Recipe
from flask_app.models.user import User
from flask import flash


@app.route('/add_recipe')
def add_recipe():

    return render_template('add_recipe.html')

@app.route('/create_recipe', methods=['POST'])
def create_recipe():
    data={
        'name' : request.form['name'],
        'min30' : request.form['min30'],
        'description' : request.form['description'],
        'instructions' : request.form['instructions'],
        'user_id' : session['user_id']
    }  
    Recipe.save(data)
    print('save recipe to user')
    return redirect('/dashboard')


#  DASHBOARD PAGE________________________________________________________________________________
# @app.route('/dashboard')
# def dashboard():

    # if 'user_id' not in session:
    #     return redirect('/')
    # all_recipes = Recipe.get_all()

    # return render_template('dashboard.html' , recipes=all_recipes )
@app.route('/dashboard')
def dashboard():

    if 'user_id' not in session:
        return redirect('/')
    data_id = {'id': session['user_id']}

    all_recipes = Recipe.get_all_users_and_recipes()
    logged_in_user = User.get_one(data_id)

    return render_template('dashboard.html' , recipes=all_recipes, logged_in_user=logged_in_user )


# EDITS RECIPES____________________________________________________________________________________
@app.route("/edit/<int:id>")
def update_recipe(id):
    print("the info from html form to substitute to update with")
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id":id
    }
    Recipe.get_one(data)
    return render_template("edit_recipe.html", recipe=Recipe.get_one(data))

# DELETE THE PIE_________________________________________________________________________
@app.route("/delete/<int:id>")
def delete(id):
    data= {
    "id":id
    }
    Recipe.delete(data)
    return redirect('/dashboard')

# UPDATE THE RECIPE___________________________________________________________________________________
@app.route("/update/<int:id>", methods=['POST'])
def update(id):
    data= {
    "id":id,
    'name' : request.form['name'],
    'min30' : request.form['min30'],
    'description' : request.form['description'],
    'instructions' : request.form['instructions'],
    }
    if 'user_id' not in session:
        return redirect('/')
    # if not Recipe.validate_listing(request.form):
    #     flash("Invalid fields")
    #     return redirect(f'/update/{id}')                                            #xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    Recipe.update(data)
    print('update the pie listing')
    return redirect('/dashboard')

# VIEW SINGLE LISTING________________________________________________________________________________
@app.route('/view/<int:id>')
def view_pie(id):
    data= {
    "id":id,
    }
    if 'user_id' not in session:
        return redirect('/')
    Recipe.get_one(data)
    return render_template('view_recipe.html', recipe=Recipe.get_one(data))


