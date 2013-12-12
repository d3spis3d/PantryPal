#!/usr/bin/python
import os
import subprocess
import sys
subprocess.call(['python', 'virtualenv.py',
                 '--python=/usr.bin/python2.7', 'flask'])
if sys.platform == 'win32':
    bin = 'Scripts'
else:
    bin = 'bin'
subprocess.call([os.path.join('flask', bin, 'pip'), 'install', 'flask<0.10'])
subprocess.call([os.path.join('flask', bin, 'pip'), 'install', 'flask-login'])
if sys.platform == 'win32':
    subprocess.call([os.path.join('flask', bin, 'pip'), 'install', '--no-deps',
                     'lamson', 'chardet', 'flask-mail'])
else:
    subprocess.call([os.path.join('flask', bin, 'pip'),
                     'install', 'flask-mail'])
subprocess.call([os.path.join('flask', bin, 'pip'),
                 'install', 'sqlalchemy==0.7.9'])
subprocess.call([os.path.join('flask', bin, 'pip'),
                 'install', 'flask-sqlalchemy'])
subprocess.call([os.path.join('flask', bin, 'pip'),
                 'install', 'sqlalchemy-migrate'])
subprocess.call([os.path.join('flask', bin, 'pip'),
                 'install', 'flask-wtf'])
