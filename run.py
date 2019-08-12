from app import app
from db import db


db.init_app(app)

# in order to create table using sqlalchemy itself use a decorator and this will run before any other request in file and will go to sqlite///data.db after creating that
@app.before_first_request
def create_tables():
    db.create_all()
