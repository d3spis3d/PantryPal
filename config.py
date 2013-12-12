import os
basedir = os.path.abspath(os.path.dirname(__file__))

# Configuration for sqlite database
SQLALCHEMY_DATABASE_URI = ('sqlite:///' + os.path.join(basedir, 'app.db') +
                           '?check_same_thread=False')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

# This enables cross-site request forgery prevention in Flask-WTF.
CSRF_ENABLED = True
SECRET_KEY = 'what-ever-you-like-here'
