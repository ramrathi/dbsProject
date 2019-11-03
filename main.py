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

def auth(page):
	# Session url holds the last visited link by the user
	session['url'] = page
	if 'logged_in' in session: return True
	else: return False

def refreshcookies():
	sql = "select * from Users where id = '%s';"%(session['userid'])
	cursor.execute(sql)
	data = cursor.fetchall()
	session.clear()
	session['logged_in'] = True
	session['userid'] = data[0][0]
	session['username'] = data[0][1]
	session['dob'] = data[0][3]
	session['bio'] = data[0][5]
	session['picture'] = data[0][11]


def getfriendsposts(userdata):
	# Sorry for using cartesian products
	sql = 'select name,content,time_stamp,p_id,photosrc,p_id from Users,Posts where u_id = id and (u_id in (select u2_id from Friends where u1_id =%s) or u_id = %s)'%(session["userid"],session["userid"])
	cursor.execute(sql)
	posts = cursor.fetchall()
	posts = posts[::-1]	# Newest posts come first
	userdata['posts'] = posts
	sql = 'select comm_id,post_id, name,content,timestamp from Comments join Users on Users.id = Comments.user_id'
	cursor.execute(sql)
	comments = cursor.fetchall()
	userdata['comments'] = comments


def geteventdata(data):
	sql = "select e_id,host,location,description,mediasrc,count(*) as count from Events join Attending where Attending.event_id = Events.e_id group by e_id;"
	sql2 = "select e_id,user_id from (Events join Attending on Events.e_id = Attending.event_id) where user_id in (select u2_id from Friends where u1_id = %s);"%(session['userid'])
	data['events'] = {}
	data['event_friends'] = {}
	cursor.execute(sql)
	events = cursor.fetchall()
	cursor.execute(sql2)
	event_friends = cursor.fetchall()
	for e in events:
		data['events'][int(e[0])] = e + tuple([[x[1] for x in event_friends if x[0] == e[0]]]) ;

def getuserdata(userdata):
	userdata['username'] = session['username']
	userdata['userid'] = session['userid']
	userdata['bio'] = session['bio']
	# Currently hardcoded to the link of my fb profile picture, need to add new colun in the Users table to support and store this
	# userdata['profile_picture'] = session['picture']

def getfrienddata(userdata):
    sql = "select name from Users where id=%s;"%(session['fid'])
    sql2 = "select bio from Users where id=%s;"%(session['fid'])
    cursor.execute(sql)
    userdata['friendname'] = cursor.fetchone()[0]
    cursor.execute(sql2)
    userdata['fbio'] = cursor.fetchall()[0][0]

def getwalletdata(userdata):
	sql = "select wallet from Users where id = %s"%(session['userid'])
	cursor.execute(sql)
	wallet = cursor.fetchall()
	print(wallet[0][0])
	userdata['wallet'] = wallet[0]

def getuserfriends(userdata):
	# Overcomplicated query for extra marks ;)
	sql = "select y.name,u2_id from Users join Friends on (Users.id = Friends.u1_id) join (select u2_id,name from Users join Friends on (Users.id = Friends.u2_id)) as y using(u2_id) where id = %s;"%(userdata['userid'])
	cursor.execute(sql)
	friends = cursor.fetchall()
	userdata['friends'] = friends
	# print(friends)

def getallusers(data):

	# Gets users which aren't already friends with current user
	sql = "select id,name from Users where id not in (select u2_id from Friends where u1_id = %s) and id <> %s and id not in (select u_id2 from Requests where u_id1 = %s);"%(session["userid"],session["userid"],session["userid"])
	cursor.execute(sql)
	data["otherusers"] = cursor.fetchall()

def getfriendrequests(data):

	# Gets all the friend requests for current user
	sql = "select u_id1,name from Requests join Users on Users.id = Requests.u_id1 where u_id2 = %s"%(session["userid"])
	cursor.execute(sql)
	data["requests"] = cursor.fetchall()

def getmessages(messages):
    sql = "select m.m_id,m.From,m.Content,m.media,m.timestamp from Messages m where m.m_id in(select m1.m_id from Messages m1 where m1.To=%s and m1.From=%s UNION select m1.m_id from Messages m1 where m1.To=%s and m1.From=%s);"%(session["userid"],session["fid"],session["fid"],session["userid"])
    cursor.execute(sql)
    messages['texts'] = cursor.fetchall()
    messages['users'] = []
    for i in messages['texts']:
        print("id=")
        print(i[1])
        sql2 = "select name from Users where id=%s;"%(i[1])
        cursor.execute(sql2)
        n = cursor.fetchall()[0][0]
        messages['users'].append(n)
    print(messages['users'])
    print(messages['texts'])

@app.route('/',methods=['GET'])
def home():
	# If user not logged in
	if not auth("/"): return redirect('/login')
	# Get all the details to display first and then render
	session['url']='/'
	userdata = {}
	getuserdata(userdata)
	getuserfriends(userdata)
	getallusers(userdata)
	getfriendsposts(userdata)
	getfriendrequests(userdata)
	# print(userdata["posts"])
	return render_template("./home.html",userdata = userdata)

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
			session['picture'] = data[0][11]
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



@app.route('/myprofile',methods=['GET','POST'])
def myprofile():
	if not auth("/myprofile"): return redirect('/login')
	if request.method == 'GET':
		# Get posts made by current user
		sql = 'select content,time_stamp,p_id,photosrc from Posts where u_id = %s;'%(session['userid'])
		cursor.execute(sql)
		posts = cursor.fetchall()
		posts = posts[::-1]	# Newest posts come first
		userdata={}
		userdata['posts'] = posts
		getuserdata(userdata)
		getuserfriends(userdata)
		getallusers(userdata)
		return render_template("./profile.html",userdata = userdata)
	else:
		status = request.form['status']
		picture = request.form['picture']
		if status:
			sql = "update Users set bio = '%s' where id = %s"%(status,session['userid'])
			print(sql)
			session['status'] = status
			cursor.execute(sql)
		if picture:
			sql = "update Users set picture = '%s' where id = %s"%(picture,session['userid'])
			print(sql)
			session['status'] = status
			cursor.execute(sql)

		mydb.commit()
		refreshcookies()
		return redirect('/myprofile')


@app.route('/logout',methods=['POST','GET'])
def logout():
	# DESTROYED.
	session.clear()
	return redirect('/login')

@app.route('/post',methods=['POST'])
def post():
	content = request.form['content']

	f = request.files['picture']
	if f:
		f.save('static/'+f.filename)
		sql = "INSERT INTO `dbsproject`.`Posts` (`u_id`, `content`, `time_stamp`,`photosrc`) VALUES ('%s', '%s', CURTIME(),'static/%s');"%(session['userid'],content,f.filename)
		cursor.execute(sql)
	else:
		sql = "INSERT INTO `dbsproject`.`Posts` (`u_id`, `content`, `time_stamp`) VALUES ('%s', '%s', CURTIME());"%(session['userid'],content)
		cursor.execute(sql)
	mydb.commit()
	# Refresh, so that post is seen
	return redirect("/")

@app.route('/market',methods=['GET','POST'])
def market():
	if request.method =='POST':
		content = request.form['content']
		sql = "INSERT INTO `dbsproject`.`Posts` (`u_id`, `content`, `time_stamp`) VALUES ('%s', '%s', CURTIME());"%(session['userid'],content)
		cursor.execute(sql)
		mydb.commit()
		# Refresh, so that post is seen
		return redirect("/market")
	else:
		if not auth("/market"): return redirect('/login')
		sql = 'select i_id,title,description,price,Users.name,seller from Market join Users on Users.id = Market.seller where sold = 0'
		cursor.execute(sql)
		items = cursor.fetchall()
		data = {}
		data['items'] = items
		data['userdata'] = {}
		getuserdata(data['userdata'])
		getuserfriends(data['userdata'])
		print(data['userdata']['userid'] == data['items'][-1][5])
		return render_template('market.html',data=data)


@app.route('/marksold/<string:id>', methods=['GET'])
def marksold(id):
	sql = 'UPDATE Market set sold= 1 where i_id = %s'%(id)
	cursor.execute(sql)
	mydb.commit()
	return redirect('/market')

@app.route('/buy/<string:id>', methods=['GET'])
def buy(id):

	# Opportunity to put a trigger or something, if the
	# wallet value in Users goes negative then reset the sold
	# and wallet. Basically don't sell it then

	sql = 'UPDATE Market set sold= 1 where i_id = %s'%(id)
	sql2 = 'UPDATE Users set wallet = wallet - (select price from Market where i_id = %s) where id = %s'%(id,session['userid'])
	cursor.execute(sql)
	cursor.execute(sql2)
	mydb.commit()
	return redirect('/market')

@app.route('/requests/<string:choice>/<string:id>', methods=['GET'])
def requests(choice,id):
	if choice == "add":
		sql = "insert into Friends values (%s,%s)"%(id,session['userid'])
		cursor.execute(sql)
		sql = "insert into Friends values (%s,%s)"%(session['userid'],id)
		cursor.execute(sql)
	sql = "delete from Requests where u_id1 = %s"%(id)
	cursor.execute(sql)
	mydb.commit()
	return redirect(session['url'])

@app.route('/friends/<string:choice>/<string:id>', methods=['GET'])
def friends(choice,id):

	if choice == "add":
		sql = "insert into Requests values (%s,%s)"%(session['userid'],id)
		cursor.execute(sql)
	else:
		sql = "delete from Friends where (u1_id = %s and u2_id = %s) or (u1_id = %s and u2_id = %s) "%(id,session['userid'],session['userid'],id)
		cursor.execute(sql)
	mydb.commit()
	return redirect(session['url'])

@app.route('/posts/<string:action>/<string:id>', methods=['GET'])
def posts(action,id):
	if action=='delete':
		sql = 'delete from Posts where p_id = %s'%(id)
		cursor.execute(sql)
		mydb.commit()
		return redirect(session['url'])

@app.route('/events', methods=['GET'])
def events():
	if request.method == 'GET':
		if not auth('/events'): return redirect('/login')
		data = {}
		data['events'] = {}
		data['userdata'] = {}
		geteventdata(data['events'])
		getuserdata(data['userdata'])
		return render_template("./events.html",data = data)

@app.route('/comment/<string:action>/<string:id>', methods=['POST','GET'])
def comment(action,id):
	if request.method == 'POST':
		comment_content = request.form['content']
		sql = "insert into Comments values (NULL,'%s','%s','%s',NULL)"%(id,session['userid'],comment_content)
		cursor.execute(sql)
		mydb.commit()
		return redirect('/')
	else:
		sql = "delete from Comments where comm_id = %s"%(id)
		cursor.execute(sql)
		mydb.commit()
		return redirect('/')


@app.route('/transaction', methods=['POST','GET'])
def transaction():
	if request.method == 'GET':
		if not auth("/transaction"): return redirect('/login')
		userdata = {}
		getwalletdata(userdata)
		getuserdata(userdata)
		getuserfriends(userdata)
		return render_template('./transaction.html',userdata=userdata)
	else:
		if not auth("/transaction"): return redirect('/login')
		f_id = request.form["friends"]	
		amount = request.form["amount"]	


@app.route('/chats/<string:id>', methods=['GET'])
def chat_message(id):
    if not auth("/"): return redirect('/login')
    if int(id):
        session['fid'] = id
    print("this is "+ session['fid'])
    userdata = {}
    messages = {}
    getmessages(messages)
    print(messages)
    getuserdata(userdata)
    getfrienddata(userdata)
    getuserfriends(userdata)
    getallusers(userdata)
    getfriendsposts(userdata)
    getfriendrequests(userdata)
    return render_template('./chat.html',userdata=userdata, messages=messages)

@app.route('/chatstore', methods=['POST'])
def chatstore():
    print("HERE")
    if session['fid']:
        content = request.form['content']
        sql = "INSERT INTO `dbsproject`.`Messages` (`From`, `To`, `Content`, `timestamp`) VALUES ('%s', '%s', '%s', CURTIME());"%(session['userid'],session['fid'],content)
        cursor.execute(sql)
        mydb.commit()
        return redirect(url_for('chat_message', id=session['fid']))

if __name__ == "__main__":
    app.run(port=3000, debug=True)
