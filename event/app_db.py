"""control dependencies to support CRUD app routes and APIs"""
from flask import Blueprint, render_template, request, url_for, redirect, jsonify, make_response
from flask_restful import Api, Resource
import requests
from event.model import Events

# blueprint defaults https://flask.palletsprojects.com/en/2.0.x/api/#blueprint-objects
app_db = Blueprint('event', __name__,
                     url_prefix='/event',
                     template_folder='templates/crud/',
                     static_folder='static',
                     static_url_path='assets')

# API generator https://flask-restful.readthedocs.io/en/latest/api.html#id1
api = Api(app_db)

""" Application control for CRUD is main focus of this File, key features:
    1.) event table queries
    2.) app routes (Blueprint)
    3.) API routes
    4.) API testing
"""

""" events table queries"""


# events extraction from SQL
def event_all():
    """converts event table into JSON list """
    return [peep.read() for peep in Events.query.all()]


# event extraction from SQL
def event_by_id(id):
    """finds User in table matching userid """
    return Events.query.filter_by(eventID=id).first()


# User extraction from SQL
def event_by_event(ev):
    """finds User in table matching fav_res """
    return Events.query.filter_by(event=ev).first()


""" app route section """


# Default URL
@app_db.route('/')
def crud():
    """obtains all event from table and loads Admin Form"""
    return render_template("database.html", table=event_all())


# CRUD create/add
@app_db.route('/create/', methods=["POST"])
def create():
    """gets data from form and add it to Users table"""
    if request.form:
        po = Events(
            request.form.get("date"),
            request.form.get("event"),
            request.form.get("description"),
        )
        po.create()
    return redirect(url_for('event.crud'))


# CRUD read
@app_db.route('/read/', methods=["POST"])
def read():
    """gets userid from form and obtains corresponding data from Users table"""
    table = []
    if request.form:
        ev = request.form.get("eventID")
        po = event_by_id(ev)
        if po is not None:
            table = [po.read()]  # placed in list for easier/consistent use within HTML
    return render_template("database.html", table=table)


# CRUD update
@app_db.route('/update/', methods=["POST"])
def update():
    """gets userid and name from form and filters and then data in  Users table"""
    if request.form:
        ev = request.form.get("eventID")
        event = request.form.get("event")
        po = event_by_id(ev)
        if po is not None:
            po.update(event)
    return redirect(url_for('event.crud'))


# CRUD delete
@app_db.route('/delete/', methods=["POST"])
def delete():
    """gets userid from form delete corresponding record from Users table"""
    if request.form:
        id = request.form.get("eventID")
        po = event_by_id(id)
        if po is not None:
            po.delete()
    return redirect(url_for('event.crud'))


""" API routes section """


class EventsAPI:
    # class for create/post
    class _Create(Resource):
        def post(self, date, event, description):
            po = Events(date, event, description)
            ev = po.create()
            if ev:
                return ev.read()
            return {'message': f'Processed {event}'}, 210

    # class for read/get
    class _Read(Resource):
        def get(self):
            return event_all()

    # class for update/put
    class _Update(Resource):
        def put(self, date, event, description):
            po = event_by_event(date, event, description)
            if po is None:
                return {'message': f"{event} not found"}, 210
            po.update(event)
            return po.read()

    # class for delete
    class _Delete(Resource):
        def delete(self, id):
            po = event_by_id(id)
            if po is None:
                return {'message': f"{id} is not found"}, 210
            data = po.read()
            po.delete()
            return data

    # building RESTapi resource
    api.add_resource(_Create, '/create/<string:date>/<string:event>/<string:description>')
    api.add_resource(_Read, '/read/')
    api.add_resource(_Update, '/update/<string:date>/<string:event>/<string:description>')
    api.add_resource(_Delete, '/delete/<int:eventID>')


""" API testing section """


def api_tester():
    # local host URL for model
    url = 'http://localhost:5222/crud'

    # test conditions
    API = 0
    METHOD = 1
    tests = [
        ['/create/Wilma Flintstone/wilma@bedrock.org/123wifli/0001112222', "post"],
        ['/create/Fred Flintstone/fred@bedrock.org/123wifli/0001112222', "post"],
        ['/read/', "get"],
        ['/update/wilma@bedrock.org/Wilma S Flintstone/123wsfli/0001112229', "put"],
        ['/update/wilma@bedrock.org/Wilma Slaghoople Flintstone', "put"],
        ['/delete/4', "delete"],
        ['/delete/5', "delete"],
    ]

    # loop through each test condition and provide feedback
    for test in tests:
        print()
        print(f"({test[METHOD]}, {url + test[API]})")
        if test[METHOD] == 'get':
            response = requests.get(url + test[API])
        elif test[METHOD] == 'post':
            response = requests.post(url + test[API])
        elif test[METHOD] == 'put':
            response = requests.put(url + test[API])
        elif test[METHOD] == 'delete':
            response = requests.delete(url + test[API])
        else:
            print("unknown RESTapi method")
            continue

        print(response)
        try:
            print(response.json())
        except:
            print("unknown error")


def api_printer():
    print()
    print("Events table")
    for ev in event_all():
        print(wv)


"""validating api's requires server to be running"""
if __name__ == "__main__":
    api_tester()
    api_printer()
