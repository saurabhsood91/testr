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
    role = db.StringField(default='')
    username = db.StringField()
    password = db.StringField()
    emailId = db.StringField()

class Course(db.Document):
    instructor = db.StringField(default='')
    course_id = db.StringField()
    course_name = db.StringField()

class Test(db.Document):
    course_id = db.StringField()
    test_name = db.StringField()
    questions = db.ListField(db.StringField())

class Questions(db.Document):
    question = db.StringField()
    reference_answer = db.StringField()
    tags = db.ListField(db.StringField(), default= [])
    options = db.ListField(db.StringField(), default= [])



def authenticate(username, password):
    user = User.query.filter(User.username == username).first();
    if user and check_password_hash(user.password,password):
        user.id = str(user.mongo_id)
        return user


def identity(payload):
    user_id = payload['identity']
    user = User.query.filter(User.mongo_id == user_id).first();
    return user.mongo_id

jwt = JWT(app, authenticate, identity)


@app.route('/protected')
@jwt_required()
def protected():
    return '%s' % current_identity


@app.route('/',methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/addCourse', methods=['POST'])
def add_course():
    data = json.loads(request.data.decode())
    course_id= data['course_id']
    course_name=  data['course_name']
    new_course = Course(course_id=course_id, course_name = course_name)
    new_course.save()
    return json.dumps({"auth":"1"})


@app.route('/showInstructors', methods=['POST'])
def show_instructors():
    resultSet= User.query.filter(User.role == 'instructor').all()
    for each in resultSet:
        test_names.append({"Username":each.username, "Email":each.emailId})
    return json.dumps(test_names)

@app.route('/assignAsInstructor', methods=['POST'])
def assign_as_instructor():
    data = json.loads(request.data.decode())
    pairs = data['pairs']
    for pair  in pairs:
        res = User.query.filter(User.username == pair['username'])
        res.set(User.role,'instructor').execute()
        res = Course.query.filter(Course.course_id == pair['course_id'])
        res.set(Course.instructor, pair['username']).execute()
        return json.dumps({"auth":"1"})

@app.route('/addtest', methods=['POST'])
def add_test():
    data = json.loads(request.data.decode())
    test_name = data['test_name']
    course_id = data['course_id']
    questions = data['questions']

    question_ids = []

    for question in questions:
        if question.get('id') != None:
            id = question['id']
            question_ids.append(id)
        else:

            question_type = question['type']
            actual_question = question['question']
            reference_answer = question.get('reference_answer')
            tags = question.get('tags')
            options = question.get('options')

            question_object = Questions(question=actual_question, reference_answer=reference_answer, tags=tags, options=options)

            question_object.save()
            question_ids.append(str(question_object.mongo_id))

            test_object = Test(course_id= course_id, test_name=test_name, questions = question_ids) 
            test_object.save()

    return json.dumps({"test_id":str(question_object.mongo_id)})

@app.route('/viewbycourse', methods=['POST'])
def view_by_course():
    data = json.loads(request.data.decode())
    test_names = []
    course_id = data['course_id']
    resultSet= Test.query.filter(Test.course_id == course_id).all()

    for each in resultSet:
        test_names.append({"course_id":each.course_id, "test_name":each.test_name})
    return json.dumps(test_names)

@app.route('/register',methods=['POST'])
def register():
    if request.method == 'POST':
        username = request.json['username']
        password = request.json['password']
        emailID = request.json['emailID']

        checkUserName = User.query.filter(User.username == username).first()
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
    checkUserName = User.query.filter(User.mongo_id == userID).first()
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
        checkUserName = User.query.filter(User.username == username).first()

        if check_password_hash(checkUserName.password, password):
            print "Username Password Matched"
            flash('Logged in');
            #return render_template('404.html'), 500
            return json.dumps({'auth': 1})
        else:
            print "Remember your password you fool!"
            flash('Remember your password you fool!')
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
