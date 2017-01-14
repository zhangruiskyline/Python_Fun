
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import make_response
from flask import Flask, session, redirect, url_for, escape, request
from flask import render_template
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:test123@localhost/flaskmovie'
app.config['SECRET_KEY'] = 'super-secret'
app.config['SECURITY_REGISTERABLE'] = True

#app.debug = True
db = SQLAlchemy(app)

user = {}

# Define models
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

#Route these to the same function
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
