import os
import mysql.connector
from os.path import join, dirname
from dotenv import load_dotenv
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
app = Flask(__name__)
app.secret_key = "fuck off"


def getfriendsposts(userdata):
	# Sorry for using cartesian products
	sql = 'select name,content,time_stamp from Users,Posts where u_id = id and (u_id in (select u2_id from Friends where u1_id =%s) or u_id = %s)'%(session["userid"],session["userid"])
	cursor.execute(sql)
	posts = cursor.fetchall()
	posts = posts[::-1]	# Newest posts come first
	userdata['posts'] = posts


def getuserdata(userdata):
	userdata['username'] = session['username']
	userdata['userid'] = session['userid']
	userdata['bio'] = session['bio']

	# Currently hardcoded to the link of my fb profile picture, need to add new colun in the Users table to support and store this
	userdata['profile_picture'] = "https://scontent.fbom2-1.fna.fbcdn.net/v/t1.0-1/c0.0.160.160a/p160x160/20800338_1612121165488974_8186128540972407853_n.jpg?_nc_cat=108&_nc_oc=AQnw-asYoiVxRkjzRh1SouPuHhZTJUT6-Mc7jse-PMFsqVGj2D9S1YBzWvZawevztDY&_nc_ht=scontent.fbom2-1.fna&oh=8adb94eb5871b5464e14f1742a56dce4&oe=5E1FD366"

def getuserfriends(userdata):

	# Overcomplicated query for extra marks ;)
	sql = "select y.name,u2_id from Users join Friends on (Users.id = Friends.u1_id) join (select u2_id,name from Users join Friends on (Users.id = Friends.u2_id)) as y using(u2_id) where id = %s;"%(userdata['userid'])
	cursor.execute(sql)
	friends = cursor.fetchall()
	userdata['friends'] = friends
	print(friends)

def getallusers(data):

	# Gets users which aren't already friends with current user
	sql = "select id,name from Users where id not in (select u2_id from Friends where u1_id = %s) and id <> %s;"%(session["userid"],session["userid"])
	cursor.execute(sql)
	data["otherusers"] = cursor.fetchall()


@app.route('/',methods=['GET'])
def home():

	# If user already logged in 
	if 'logged_in' in session: 

		# Get all the details to display first and then render
		userdata = {}
		getuserdata(userdata)
		getuserfriends(userdata)
		getallusers(userdata)
		getfriendsposts(userdata)	
		print(userdata["posts"])	

		return render_template("./home.html",userdata = userdata)

	# Not logged in 
	else :
		return redirect('/login')

@app.route('/login',methods=['GET','POST'])
def login():
	if request.method == 'POST':
		email = request.form["email"]
		password = request.form["password"]
		sql = "select * from Users where email = '%s' and password = '%s';"%(email,password)
		cursor.execute(sql)
		data = cursor.fetchall()
		
		# If it can't find an account with matching credentials
		if len(data)==0:
			print("Wrong password")
			return render_template('./index.html',error = "Wrong email or password")
		
		# Account found
		else:
			# Set session variables, have only added a few for now
			session['logged_in'] = True
			session['userid'] = data[0][0]
			session['username'] = data[0][1]
			session['dob'] = data[0][3]
			session['bio'] = data[0][5]
			return redirect('/')
	else:
		# If GET and already logged in, just redirect
		if 'logged_in' in session:
			return redirect('/')
		# If not logged in show login page
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



@app.route('/myprofile',methods=['GET'])
def myprofile():
	userdata = {}
	# Get posts made by current user
	sql = 'select content,time_stamp from Posts where u_id = %s;'%(session['userid'])
	cursor.execute(sql)
	posts = cursor.fetchall()
	posts = posts[::-1]	# Newest posts come first
	userdata={}
	userdata['posts'] = posts	
	getuserdata(userdata)
	getuserfriends(userdata)
	getallusers(userdata)
	return render_template("./profile.html",userdata = userdata)

@app.route('/logout',methods=['POST','GET'])
def logout():
	# DESTROYED.
	session.clear()
	return redirect('/login')

@app.route('/post',methods=['POST'])
def post():
	content = request.form['content']
	sql = "INSERT INTO `dbsproject`.`Posts` (`u_id`, `content`, `time_stamp`) VALUES ('%s', '%s', CURTIME());"%(session['userid'],content)
	cursor.execute(sql)
	mydb.commit()
	# Refresh, so that post is seen
	return redirect("/")



if __name__ == "__main__":
    app.run(port=3000, debug=True)