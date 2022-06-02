""" database dependencies to support Users db examples """
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_migrate import Migrate

from __init__ import app

# Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into Python shell and follow along
# Define variable to define type of database (sqlite), and name and location of myDB.db
dbURI = 'sqlite:///model/myDB.db'
# Setup properties for the database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = dbURI
app.config['SECRET_KEY'] = 'SECRET_KEY'
# Create SQLAlchemy engine to support SQLite dialect (sqlite:)
db = SQLAlchemy(app)
Migrate(app, db)


# Define the Users table within the model
# -- Object Relational Mapping (ORM) is the key concept of SQLAlchemy
# -- a.) db.Model is like an inner layer of the onion in ORM
# -- b.) Users represents data we want to store, something that is built on db.Model
# -- c.) SQLAlchemy ORM is layer on top of SQLAlchemy Core, then SQLAlchemy engine, SQL
class Events(db.Model):
    # define the Events schema
    eventID = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), unique=False, nullable=False)
    event = db.Column(db.String(255), unique=False, nullable=False)
    description = db.Column(db.String(255), unique=False, nullable=False)

    # constructor of a event object, initializes of instance variables within object
    def __init__(self, date, event, description):
        self.date = date
        self.event = event
        self.description = description

    # create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a person object from Users(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "eventID": self.eventID,
            "date": self.date,
            "event": self.event,
            "description": self.description,
        }

    # update: updates users name, res, food
    # returns self
    def update(self, date, event="", description=""):
        """only updates values with length"""
        if len(event) > 0:
            self.event = event
        if len(description) > 0:
            self.description = description

        self.date = date

        db.session.commit()
        return self

    # CRUD delete: remove self
    # None
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None


"""Database Creation and Testing section"""


def model_tester():
    print("--------------------------")
    print("Seed Data for Table: users")
    print("--------------------------")
    db.create_all()
    """Tester data for table"""
    u1 = Events(date="05/31/2022", event='orientation', description='Attend orientation ....')
    u2 = Events(date="04/01/2022", event='graduation', description='graduation details ....')

    table = [u1, u2]
    for row in table:
        try:
            db.session.add(row)
            db.session.commit()
        except IntegrityError:
            db.session.remove()



def model_printer():
    print("------------")
    print("Table: event with SQL query")
    print("------------")
    result = db.session.execute('select * from events')
    print(result.keys())
    for row in result:
        print(row)


if __name__ == "__main__":
    model_tester()  # builds model of events
    model_printer()
