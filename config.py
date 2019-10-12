import os
import psycopg2
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, 'app.db')
	
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    SQLALCHEMY_TRACK_MODIFICATIONS = False