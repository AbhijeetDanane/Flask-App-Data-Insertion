import email_validator
from logging import error
from flask import Flask, url_for, render_template, flash, request, redirect, session,logging,request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, IntegerField,EmailField)
from wtforms.validators import InputRequired, Length, Email


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class User(db.Model):
	""" Create user table"""
	id = db.Column(db.Integer, primary_key=True)
	firstname = db.Column(db.String(80))
	lastname = db.Column(db.String(80))
	email = db.Column(db.String(20))
	contact_number = db.Column(db.String(20))
	gender = db.Column(db.String(10))
	
	def __init__(self, firstname, lastname,email,contact_number,gender):
		self.firstname = firstname
		self.lastname = lastname
		self.email = email
		self.contact_number = contact_number
		self.gender = gender


class Registartionform(FlaskForm):
	firstname = TextAreaField("First Name",validators=[InputRequired("Please enter your first name."),Length(min=2, max=15)]),
	lastname =TextAreaField("Last Name",validators=[InputRequired("Please enter your last name."),Length(min=2, max=15)]),
	email = TextAreaField("Email",validators=[InputRequired("Please enter your email address."),Email()]),
	contact_number = IntegerField("Email",validators=[InputRequired()]),		


@app.route('/', methods=['GET', 'POST'])
def home():
	form = Registartionform(request.form)	
	if request.method == 'POST':
		if form.validate():           		
			new_user = User(firstname=request.form['firstname'],
					lastname=request.form['lastname'],
					email=request.form['email'],
					contact_number=request.form['contact_number'],
					gender=request.form['gender'])		
			db.session.add(new_user)
			db.session.commit()			
		return redirect(url_for('thankyou'))
	
	return render_template('register.html',form = form)
	
@app.route('/thankyou', methods=['GET', 'POST'])
def thankyou():
	"""thankyou Form"""
	if request.method == 'GET':
		return render_template('thankyou.html')



if __name__ == '__main__':
	app.debug = True
	db.create_all()
	app.secret_key = "123"
	app.run(host='0.0.0.0')
	
