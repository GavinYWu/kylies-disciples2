# import "packages" from flask
from flask import Flask, render_template

# create a Flask instance
app = Flask(__name__)


# connects default URL to render index.html
@app.route('/')
def index():
    return render_template("index.html")


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


@app.route('/login/')
def login():
    return render_template("login.html")


@app.route('/logout/')
def logout():
    return render_template("logout.html")


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
    return render_template("holidaydec.html")

# runs the application on the development server
if __name__ == "__main__":
    app.run(debug=True)
