import os
from flask import Flask, render_template, request, redirect
import urllib.request
from flask import send_file
import sqlite3
from flask import g

salt = "TwinFuries"

app=Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

DATABASE = os.path.join(APP_ROOT,'database/database.db')

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

@app.route('/init_db')
def init_db():
   with app.app_context():
       db = get_db()
       with app.open_resource('schema.sql', mode='r') as f:
           db.cursor().executescript(f.read())
       db.commit()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def execute_db(query):
    cur = get_db()
    cur.execute(query)
    cur.commit()
    cur.close()

@app.route('/', methods = ['GET','POST'])
def home():
	# init_db()
	return render_template('home.html')

@app.route('/login', methods = ['GET','POST'])
def login():
	if request.method == 'POST':
		email = request.form['username']
		password = request.form['password']
		c=get_db()
		cur=c.cursor()
		passwordFromDB = query_db('select pass from customerDetails where email ="'+email+'"')
		if password==passwordFromDB[0][0]:
			return render_template('orderForm.html')
		else:
			message="Incorrect Credentials"
			return render_template('login.html', confirm=message)
	return render_template('login.html')

@app.route('/register', methods = ['GET','POST'])
def register():
	if request.method == 'POST':
		email = request.form['email']
		name = request.form['name']
		number = request.form['number']
		address = request.form['address']
		password = request.form['password']
		execute_db('insert into customerDetails values("'+email+'","'+name+'","'+number+'","'+address+'","'+password+'")')
		return render_template('orderForm.html')
	return render_template('register.html')

@app.route('/orderForm', methods = ['GET','POST'])
def order():
	if request.method == 'POST':
		email = request.form['email']
		name = request.form['name']
		number = request.form['number']
		address = request.form['address']
		plates = request.form['plates']
		dish=request.form['dish']
		print(dish)
		totalPrice=int(0)
		if(dish=='nim'):
			totalPrice=100*int(plates)
		elif(dish=='sim'):
			totalPrice=70*int(plates)
		elif(dish=='c'):
			totalPrice=120*int(plates)
		else:
			totalPrice=50*int(plates)
		message = "Order Placed! Total Price = Rs. "+str(totalPrice)+"/-"
		return render_template('orderForm.html', confirm=message)
	return render_template('orderForm.html')


if __name__ == '__main__':
	app.run(debug=True)
