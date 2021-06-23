from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models.login import Login
from flask_app.models.recipe import Recipe

@app.route('/recipes')
def exam_index():
    if not "user_id" in session:
        return redirect('/')

    recipes = Recipe.get_all_recipes()

    return render_template('success.html', recipes = recipes)

@app.route('/recipes/create')
def create_recipe():
    if not "user_id" in session:
        return redirect('/')

    return render_template('create.html')

@app.route('/recipes/new_recipe', methods=['POST'])
def new_recipe():
    
    if Recipe.validate_recipe(request.form):
        data = {
            'recipe_name': request.form['recipe_name'],
            'recipe_description': request.form['recipe_description'],
            'recipe_instructions': request.form['recipe_instructions'],
            'date_created': request.form['date_created'],
            'under_30': request.form['under_30'],
            'creator_id': session['user_id']
        }

        Recipe.new_recipe(data)
        return redirect('/recipes')

    return redirect('/recipes/create')

@app.route('/recipes/<int:recipe_id>')
def recipe_show(recipe_id):

    data = {
        'id': recipe_id
    }

    recipe = Recipe.get_recipe_by_id(data)

    if recipe == False:
        return redirect('/recipes')

    return render_template('recipe.html', recipe = recipe)

@app.route('/recipes/<int:recipe_id>/edit')
def edit_recipe(recipe_id):
    data = {
        'id': recipe_id
    }

    recipe = Recipe.get_recipe_by_id(data)

    if recipe == False:
        return redirect('/recipes')
    if recipe.creator.id != session['user_id']:
        return redirect('/recipes')

    return render_template('edit_recipe.html', recipe = recipe)

@app.route('/recipes/<int:recipe_id>/update', methods=['POST'])
def update_recipe(recipe_id):

    if not Recipe.validate_recipe(request.form):
        return redirect(f'/recipes/{recipe_id}/edit')

    else:
        data = {
            'recipe_name': request.form['recipe_name'],
            'recipe_description': request.form['recipe_description'],
            'recipe_instructions': request.form['recipe_instructions'],
            'date_created': request.form['date_created'],
            'under_30': request.form['under_30'],
            'recipe_id': recipe_id
        }

        Recipe.update_recipe(data)
        return redirect(f'/recipes/{recipe_id}')

@app.route('/recipes/<int:recipe_id>/delete')
def delete_recipe(recipe_id):
    data = {
        'id': recipe_id
    }

    recipe = Recipe.get_recipe_by_id(data)

    if recipe == False:
        return redirect('/recipes')
    if recipe.creator.id != session['user_id']:
        return redirect('/recipes')


    Recipe.delete_recipe(data)
    return redirect('/recipes')