from flask import Flask, render_template ,session , redirect , url_for, flash , request
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from datetime import datetime
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired #, InputRequired ,Required
from flask.ext.triangle import Triangle
from flask.ext.mongoalchemy import MongoAlchemy




app = Flask(__name__)
app.config['SECRET_KEY'] = 'N0tHingIsImpo5Sibl3'
bootstrap = Bootstrap(app)
moment = Moment(app)
Triangle(app)

#Configuration of DB
app.config['MONGOALCHEMY_DATABASE'] = 'testr'
db = MongoAlchemy(app)


class User(db.Document):
    name = db.StringField();
    password = db.StringField();
    emailId = db.StringField();


# Class name ( Type of Object )
class NameForm(Form):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


#Awesome implementation
@app.route('/',methods=['GET', 'POST'])
def index():
    #name = None
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name')
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
        #form.name.data = ''
    return render_template('index.html',current_time=datetime.utcnow(),form=form, name=session.get('name'))


@app.route('/register',methods=['POST'])
def register():
    if request.method == 'POST':
        print "HEllo"
        name = request.form['name'] ;
        password = request.form['password'] ;
        emailID = request.form['emailID'];
        print name + " " + password + " " + emailID ;
        checkUserName = User(name=name, password=password, emailID=emailID);
        checkUserName.save();
        #print name
    #User(name=)
    return render_template('404.html'), 500


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('404.html'), 500




if __name__ == '__main__':
    app.run()
