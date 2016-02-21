from flask import Flask, render_template ,session , redirect , url_for, flash , request
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from datetime import datetime
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired #, InputRequired ,Required
from flask.ext.triangle import Triangle
from flask import Flask, request, send_from_directory
from flask.ext.mongoalchemy import MongoAlchemy
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp
from werkzeug.security import generate_password_hash, check_password_hash
import json
import requests
from flask.ext.assets import Environment, Bundle

app = Flask(__name__)
assets = Environment(app)
app.config['SECRET_KEY'] = 'N0tHingIsImpo5Sibl3'
app.config['JWT_AUTH_URL_RULE'] = '/login'
app.config['MONGOALCHEMY_DATABASE'] = 'testr'
app.config['DEBUG'] = True

bootstrap = Bootstrap(app)
moment = Moment(app)
db = MongoAlchemy(app)
Triangle(app)

js = Bundle('bower_components/angular/angular.js', 'scripts/controllers/main.js', 'bower_components/angular-bootstrap/ui-bootstrap-tpls.js', 'scripts/controllers/loggedinmodalcontroller.js',
    'bower_components/angular-ui-router/release/angular-ui-router.js', 'scripts/controllers/homecontroller.js' , 'scripts/controllers/addtestcontroller.js')
assets.register('js', js)


css = Bundle('bower_components/angular-bootstrap/ui-bootstrap-csp.css', 'css/style.css', 'bower_components/bootstrap/dist/css/bootstrap.css', 'bower_components/font-awesome/css/font-awesome.css')
assets.register('css',css)
#Configuration of DB
app.config['MONGOALCHEMY_DATABASE'] = 'testr'
db = MongoAlchemy(app)
Triangle(app)

class User(db.Document):
    username = db.StringField();
    password = db.StringField();
    emailId = db.StringField();


def authenticate(username, password):
    user = User.query.filter(User.username == username).first();
    if user and check_password_hash(user.password,password):
        user.id = str(user.mongo_id)
        return user


def identity(payload):
    user_id = payload['identity']
    user = User.query.filter(User.mongo_id == user_id).first();
    return user.mongo_id;

jwt = JWT(app, authenticate, identity)


@app.route('/protected')
@jwt_required()
def protected():
    return '%s' % current_identity


@app.route('/',methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/register',methods=['POST'])
def register():
    if request.method == 'POST':
        username = request.json['username'] ;
        password = request.json['password'] ;
        emailID = request.json['emailID'];

        checkUserName = User.query.filter(User.username == username).first();
        #print checkUserName

        if checkUserName != None :
            #checkUserName.remove();
            return json.dumps({'auth': 0})

        #print username + " " + password + " " + emailID ;
        checkUserName = User(username=username, password=generate_password_hash(password), emailId=emailID);
        #print checkUserName
        checkUserName.save();
    # return render_template('404.html'), 500
    return json.dumps({'auth': 1})

@app.route('/test',methods=['GET'])
def test():
    authorizationCode = request.headers['Authorization'];
    userID = identity(jwt.jwt_decode_callback(authorizationCode.split(" ")[1]))
    checkUserName = User.query.filter(User.mongo_id == userID).first();
    if ( checkUserName != None ):
        return render_template('404.html'), 501

    #print identity(authorizationCode.split(" ")[1])
    #print identity(jwt.jwt_decode_callback(authorizationCode.split(" ")[1]))
    return render_template('404.html'), 500


@app.route('/login',methods=['POST'])
def login():
    if request.method == 'POST':
        data =json.loads(request.data.decode())
        username = data['username']
        password = data['password']
        checkUserName = User.query.filter(User.username == username).first();

        if check_password_hash(checkUserName.password, password):
            print "Username Password Matched";
            flash('Logged in');
            #return render_template('404.html'), 500
            return json.dumps({'auth': 1})
        else:
            print "Remember your password you fool!";
            flash('Remember your password you fool!');
            #return render_template('404.html'), 500
            return json.dumps({'auth': 0})

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('404.html'), 500



@app.route('/templates/<path>')
def loggedinmodal(path):
    return render_template(path)



if __name__ == '__main__':
    app.run()
