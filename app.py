from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://{user}:{password}@{server}/{database}'.format(
    user='root', password='root', server='localhost', database='pp_orm')
db = SQLAlchemy(app)

engine = db.engine
Base = db.Model

@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()


