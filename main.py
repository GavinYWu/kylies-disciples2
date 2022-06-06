# import "packages" from flask
from flask import Flask, render_template, request
import requests, json
from __init__ import app

# from holidaydecor.app_crud import app_crud
# app.register_blueprint(app_crud)
#
# from event.app_db import app_db
# app.register_blueprint(app_db)

from cruddy.app_crud import app_crud
app.register_blueprint(app_crud)

# connects default URL to render index.html
@app.route('/')
def index():
    return render_template("index.html")


@app.route('/pagelayout/')
def pl():
    return render_template("layouts/pagelayout.html")


# connects /kangaroos path to render kangaroos.html
@app.route('/kangaroos/')
def kangaroos():
    return render_template("kangaroos.html")
 

@app.route('/walruses/')
def walruses():
    return render_template("walruses.html")


@app.route('/hawkers/')
def hawkers():
    return render_template("hawkers.html")


@app.route('/stub/')
def stub():
    return render_template("stub.html")


@app.route('/feedback/')
def feedback():
    return render_template("Feedback.php")


@app.route('/suggest/')
def suggest():
    return render_template("suggest.html")


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


@app.route('/holidaydec/')
def holidaydec():
    return render_template("reddit.html")


@app.route('/calendar/')
def calendar():
    return render_template("calendar.html")


@app.route('/ideas/')
def ideas():
    return render_template("Ideas.html")


@app.route('/newsletter/')
def newsletter():
    return render_template("newsletter.html")


@app.route('/calendar2/')
def calen():
    return render_template("calendarevent.html")


# runs the application on the development server
if __name__ == "__main__":
    app.run(debug=True)
