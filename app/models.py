from app import db


ROLE_GUEST = 0
ROLE_USER = 1


class RI_Link(db.Model):
    r_id = db.Column(db.Integer, db.ForeignKey('recipe.id'),
                     primary_key = True)
    i_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'),
                     primary_key = True)
    quantity = db.Column(db.Integer, default = 0)
    q_type = db.Column(db.String(5), default = 'g')


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True)
    password = db.Column(db.String(64))
    role = db.Column(db.SmallInteger, default = ROLE_USER)

    def __repr__(self):
        return '<User %r>' %(self.username)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)


class Ingredient(db.Model):
    __tablename__ = 'ingredient'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True, unique = True)
    calories_per_ml = db.Column(db.Integer, default = 0)
    calories_per_g = db.Column(db.Integer, default = 0)
    calories_per_tbs = db.Column(db.Integer, default = 0)
    calories_per_tsp = db.Column(db.Integer, default = 0)
    calories_per_each = db.Column(db.Integer, default = 0)
    recipes = db.relationship('RI_Link')

    def __repr__(self):
        return '<Ingredient %r>' %(self.name)


class Recipe(db.Model):
    __tablename__ = 'recipe'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    type = db.Column(db.String(8), default='dinner')
    time = db.Column(db.String(6), default='normal')
    category = db.Column(db.String(10), default='other')
    serves = db.Column(db.Integer, default=1)
    calories = db.Column(db.Integer, default=0)
    method = db.Column(db.String(750))
    ingredients = db.relationship("RI_Link")

    def __repr__(self):
        return '<Recipe %r>' %(self.name)
