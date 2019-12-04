import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """
    This class is responsible for establishing the database.
    Tracking modifications is turned off.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-defininately-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    #SQLALCHEMY_ECHO=True
