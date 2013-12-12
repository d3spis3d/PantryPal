from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

from app import views, models

if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('tmp/pantrypal.log',
                                       'a', 1*1024*1024, 10)
    formatting = ('%(asctimes)s %(levelname)s: ' +
                  '%(message) [in %(pathname)s:%(lineno)d]')
    file_handler.setFormatter(logging.Formatter(formatting))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('PantryPal startup')
