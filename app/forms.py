from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, RadioField, TextAreaField
from wtforms.validators import Required, EqualTo


class LoginForm(Form):
    username = TextField('Username', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])


class RegistrationForm(Form):
    username = TextField('Username', validators=[Required()])
    password = PasswordField('Password', validators=[Required(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')


class RecipeForm(Form):
    name = TextField('Recipe Name', validators=[Required()])
    type = RadioField('Meal Type',
                      choices=[('breakie', 'Breakfast'), ('lunch', 'Lunch'),
                               ('dinner', 'Dinner'), ('snack', 'Snack'),
                               ('dessert', 'Dessert')])
    time = RadioField('Preparation Time',
                      choices=[('quick', 'Quick'), ('normal', 'Normal'),
                               ('long', 'Long')])
    category = RadioField('Meal Category',
                          choices=[('chicken', 'Chicken'), ('beef', 'Beef'),
                                   ('lamb', 'Lamb'), ('pork', 'Pork'),
                                   ('vegie', 'Vegetarian'), ('other', 'Other')
                                   ])
    serves = TextField('Serves')
    method = TextAreaField('Method', validators=[Required()])


class IngredientForm(Form):
    name = TextField('Ingredient Name', validators=[Required()])
    calories_per_ml = TextField('Cal mL')
    calories_per_g = TextField('Cal g')
    calories_per_tbs = TextField('Cal tbs')
    calories_per_tsp = TextField('Cal tsp')
    calories_per_each = TextField('Cal each')
