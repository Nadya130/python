from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://{user}:{password}@{server}/{database}'.format(
    user='root', password='root', server='localhost', database='pp_orm')


app.config['SECRET_KEY'] = 'thisissecrret'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

engine = db.engine
Base = db.Model

from controllers.user_controller import *
from controllers.credit_controller import *
# @app.route('/')
# def hello_world():
#     return 'Hello World!'


if __name__ == '__main__':
    app.debug = True
    app.run()


