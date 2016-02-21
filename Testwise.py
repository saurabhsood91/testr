from flask import Flask, render_template ,session , redirect , url_for, flash , request
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from datetime import datetime
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired #, InputRequired ,Required
from flask.ext.triangle import Triangle
from flask import Flask, request, send_from_directory
from flask.ext.assets import Environment, Bundle
from flask.ext.mongoalchemy import MongoAlchemy
import json


app = Flask(__name__)
assets = Environment(app)
app.config['SECRET_KEY'] = 'N0tHingIsImpo5Sibl3'
app.config['MONGOALCHEMY_DATABASE'] = 'testr'
app.config['DEBUG'] = True

bootstrap = Bootstrap(app)
moment = Moment(app)
Triangle(app)

js = Bundle('bower_components/angular/angular.js', 'scripts/controllers/*.js', 'bower_components/angular-bootstrap/ui-bootstrap-tpls.js')
assets.register('js', js)


css = Bundle('bower_components/angular-bootstrap/ui-bootstrap-csp.css', 'css/style.css', 'bower_components/bootstrap/dist/css/bootstrap.css')
assets.register('css',css)
#Configuration of DB
app.config['MONGOALCHEMY_DATABASE'] = 'testr'
db = MongoAlchemy(app)
Triangle(app)


class User(db.Document):
    username = db.StringField();
    password = db.StringField();
    emailId = db.StringField();

class NameForm(Form):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/',methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name')
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html',current_time=datetime.utcnow(),form=form, name=session.get('name'))


@app.route('/register',methods=['POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'] ;
        password = request.form['password'] ;
        emailID = request.form['emailID'];

        checkUserName = User.query.filter(User.username == username).first();
        #print checkUserName

        if checkUserName != None :
            #checkUserName.remove();
            return json.dumps({'auth': 0})

        #print username + " " + password + " " + emailID ;
        checkUserName = User(username=username, password=password, emailId=emailID);
        #print checkUserName
        checkUserName.save();
    # return render_template('404.html'), 500
    return json.dumps({'auth': 1})


@app.route('/login',methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'] ;
        password = request.form['password'] ;

        checkUserName = User.query.filter(User.username == username).first();

        if checkUserName.password == password:
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



@app.route('/templates/loggedinmodal.html')
def static_file():
    return render_template('loggedinmodal.html')


if __name__ == '__main__':
    app.run()
