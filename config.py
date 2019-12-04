"""
./config.py
"""

import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """
    Class Config:
        This class is for initializing a database
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-defininately-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    #SQLALCHEMY_ECHO=True
