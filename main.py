import os
import mysql.connector
from os.path import join, dirname
from dotenv import load_dotenv
from flask import request,session,redirect
from flask import *
import random

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

mydb = mysql.connector.connect(
  host=os.getenv("localhost"),
  user=os.getenv("user"),
  passwd=os.getenv("passwd"),
  database=os.getenv("database")
)

cursor = mydb.cursor()
# sql = "blah blah"
# cursor.execute(sql)
# cursor.commit() # if update
# data = cursor1.fetchall() # if select

from flask import Flask, render_template
app = Flask(__name__)

app.secret_key = "fuck off"

@app.route('/',methods=['GET'])
def home():
	if 'logged_in' in session: 
		# Get all the details to display first and then render
		sql = 'select name,content,time_stamp from Users,Posts where u_id = id;'
		cursor.execute(sql)
		posts = cursor.fetchall()
		posts = posts[::-1]	# Newest posts come first
		print(posts)	
		#-------------------------------------
		return render_template("./home.html",posts = posts)
	else :return redirect('/login')

@app.route('/login',methods=['GET','POST'])
def login():
	if request.method == 'POST':
		email = request.form["email"]
		password = request.form["password"]
		sql = "select * from Users where email = '%s' and password = '%s';"%(email,password)
		cursor.execute(sql)
		data = cursor.fetchall()
		print(data)
		if len(data)==0:
			print("Wrong password")
			return render_template('./index.html',error = "Wrong email or password")
		else:
			# Set session variables to true
			session['logged_in'] = True
			session['userid'] = data[0][0]

			return redirect('/')
	else:
		if 'logged_in' in session:
			return redirect('/')
		return render_template("./index.html")

@app.route('/register',methods=['GET','POST'])
def register():
	if request.method == "GET":
		return render_template("./register.html")
	else:
		email = request.form['email']
		username = request.form['username']
		password = request.form['password']
		# Eh frontend guy please take the input nicely
		dob = '1999-05-27'
		gender = 1
		# The wallet is being set to random as for some reason wallet is unique? someone change this lmao
		wallet = random.randrange(0,100000)
		sql = "select * from Users where email = '%s';"%email
		cursor.execute(sql)
		data = cursor.fetchall()
		if len(data)!=0:
			return render_template('./register.html',error = "User already exists!")
		else:
			# Insert user data here

			print("Adding data")
			sql = "INSERT INTO `dbsproject`.`Users` (`name`, `password`, `dob`, `gender`, `email`, `wallet`) VALUES ('%s', '%s', '%s', '%s', '%s', '%s');" %(username,password,dob,gender,email,wallet)
			cursor.execute(sql)
			mydb.commit()
			return render_template("./index.html",error = "Account succesfully created!")



@app.route('/account',methods=['GET'])
def account():
	return render_template("./profile.html")

@app.route('/logout',methods=['POST'])
def logout():
	session.clear()
	return redirect('/login')

@app.route('/post',methods=['POST'])
def post():
	content = request.form['content']
	sql = "INSERT INTO `dbsproject`.`Posts` (`u_id`, `content`, `time_stamp`) VALUES ('%s', '%s', CURTIME());"%(session['userid'],content)
	cursor.execute(sql)
	mydb.commit()
	return redirect("/")



if __name__ == "__main__":
    app.run(port=3000, debug=True)