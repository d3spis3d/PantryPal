from app import app, db, lm
from flask import render_template, flash, redirect, session, url_for, request, g
from flask import jsonify
from flask.ext.login import login_user, logout_user
from flask.ext.login import current_user, login_required
from models import User, ROLE_USER, ROLE_GUEST, Ingredient, Recipe, RI_Link
from forms import RegistrationForm, LoginForm, IngredientForm, RecipeForm


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        user = User(username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        u = form.username.data
        user = User.query.filter_by(username=u).first()
        if user is not None:
            if form.password.data == user.password:
                login_user(user)
                return redirect(request.args.get('next') or url_for('index'))
            else:
                flash('Incorrect password or username. Please try again.')
                return redirect(url_for('login'))
        else:
            return redirect(url_for('login'))
    return render_template('login.html', title='Log In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user


@app.route('/add-recipe', methods=['POST', 'GET'])
@login_required
def add_recipe():
    form = RecipeForm()
    if request.method == 'POST' and form.validate():
        recipe = Recipe(name=form.name.data, type=form.type.data,
                        time=form.time.data, category=form.category.data,
                        serves=form.serves.data, method=form.method.data)
        db.session.add(recipe)
        # Create links between recipe and all ingredients required
        for ingredient in session['ingredients']:
            find_ingredient = Ingredient.query.filter_by(name=ingredient[0]).first()
            ing_recipe_link = RI_Link(r_id=recipe.id, i_id=find_ingredient.id,
                                      quantity=ingredient[1], q_type=ingredient[2])
            recipe.ingredients.append(ing_recipe_link)
            find_ingredient.recipes.append(ing_recipe_link)
        # Add calorie value for the recipe
        calories = 0
        for ingredient in session['ingredients']:
            find_ing = Ingredient.query.filter_by(name=ingredient[0]).first()
            if ingredient[2] == 'g':
                calories += int(ingredient[1])*int(find_ing.calories_per_g)
            elif ingredient[2] == 'mL':
                calories += int(ingredient[1])*int(find_ing.calories_per_ml)
            elif ingredient[2] == 'tbs':
                calories += int(ingredient[1])*int(find_ing.calories_per_tbs)
            elif ingredient[2] == 'tsp':
                calories += int(ingredient[1])*int(find_ing.calories_per_tsp)
            elif ingredient[2] == 'each':
                calories += int(ingredient[1])*int(find_ing.calories_per_each)
        recipe.calories = int(calories/(int(recipe.serves)))
        db.session.commit()
        return redirect(url_for('index'))
    session['ingredients'] = []
    session.modified = True
    form = RecipeForm()
    return render_template('add-recipe.html', title='Add Recipe', form=form)


# Receives ajax posts of recipe ingreds to store for current recipe creation
@app.route('/add-recipe-ingredient', methods=['GET', 'POST'])
@login_required
def add_recipe_ingredient():
    if request.method == 'POST':
        name = request.json['name']
        quantity = request.json['quantity']
        q_type = request.json['q_type']
        session['ingredients'].append([name, quantity, q_type])
        session.modified = True
        return jsonify(name=name, quantity=quantity, q_type=q_type)


# Page for adding ingreds into db
@app.route('/add-ingredient', methods=['GET', 'POST'])
@login_required
def add_ingredient():
    form = IngredientForm()
    if request.method == 'POST' and form.validate():
        ingredient = Ingredient(name=form.name.data,
                                calories_per_ml=form.calories_per_ml.data,
                                calories_per_g=form.calories_per_g.data,
                                calories_per_tbs=form.calories_per_tbs.data,
                                calories_per_tsp=form.calories_per_tsp.data,
                                calories_per_each=form.calories_per_each.data)
        db.session.add(ingredient)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add-ingredient.html',
                           title='Add Ingredient',
                           form=form)


@app.route('/recipe')
@login_required
def recipe():
    return render_template('recipe.html', title='Recipes')


@app.route('/ingredient-list', methods=['POST', 'GET'])
@login_required
def ingredient_list():
    return render_template('ingredient-list.html', title='Ingredient List')


# Returns ingredient list from starting char request
@app.route('/return-ingredient-list', methods=['POST', 'GET'])
@login_required
def return_ingredient_list():
    if request.method == 'POST':
        letter = request.json['value']
        ingredients = Ingredient.query.filter(Ingredient.name.startswith(letter)).all()
        ingred_list = {}
        count = 1
        ingred_list[0] = len(ingredients)
        for i in ingredients:
            ingred_list[count] = i.name
            count += 1
        return jsonify(ingred_list)


@app.route('/recipe-list')
@login_required
def recipe_list():
    return render_template('recipe-list.html', title='Recipe List')


# Returns recipe list from starting char request
@app.route('/return-recipe-list', methods=['POST', 'GET'])
@login_required
def return_recipe_list():
    if request.method == 'POST':
        letter = request.json['value']
        recipes = Recipe.query.filter(Recipe.name.startswith(letter)).all()
        recipe_list = {}
        count = 1
        recipe_list[0] = len(recipes)
        for r in recipes:
            recipe_list[count] = r.name
            count += 1
        return jsonify(recipe_list)
