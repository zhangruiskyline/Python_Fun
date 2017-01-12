
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import make_response
from flask import Flask, session, redirect, url_for, escape, request
from flask import render_template
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

Bootstrap(app)

user = {}

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username
'''
@app.route("/")
def index(user=None):
    return render_template('index.html')
'''
@app.route("/")
@app.route("/<user>")
def index(user=None):
    if user==None:
        return render_template('index.html')
    else:
        return render_template('user.html', user=user)

@app.route("/method")
def method():
    return "Method used: %s" % request.method


@app.route("/shopping")
def shopping():
    food = ["Cheese", "Tuna", "Beef"]
    return render_template('shopping.html', food=food)


@app.route('/hello')
def hello():
    return 'Hello, World'

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

@app.route('/profile/<name>')
def profile(name):
    return render_template('profile.html', name=name)


@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'],
                       request.form['password']):
            return log_the_user_in(request.form['username'])
        else:
            error = 'Invalid username/password'
    if request.method == 'GET':
        return render_template('login.html', error=error)
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    #return render_template('login.html', error=error)
    return 'go here'

def valid_login(user,pwd):
    if user == 'user' and pwd == 'pass':
        return True
    else:
        return False

def log_the_user_in(username, pwd):
    #f = request.files['the_file']
    #f.save('./' + secure_filename(f.filename))
    return 'login in for test'

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['the_file']
        f.save('/var/www/uploads/' + secure_filename(f.filename))

if __name__ == '__main__':
    app.run()
