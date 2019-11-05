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
app.secret_key = "thisisatopsecretkey"

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

def getcommunity(comm,id):
	sql = "call curdemo('%s',@a,@b)"%(id)
	cursor.execute(sql)
	sql2 = "select @a"
	cursor.execute(sql2)
	a=cursor.fetchall()
	sql3 = "select @b"
	cursor.execute(sql3)
	b=cursor.fetchall()
	comm['id'] = id
	comm['name'] = a[0][0]
	comm['description'] = b[0][0]

def getfriendsposts(userdata):
	# Sorry for using cartesian products
	sql = 'select name,content,time_stamp,p_id,photosrc,p_id from Users,Posts where u_id = id and community is null and (u_id in (select u2_id from Friends where u1_id =%s) or u_id = %s)'%(session["userid"],session["userid"])
	cursor.execute(sql)
	posts = cursor.fetchall()
	posts = posts[::-1]	# Newest posts come first
	userdata['posts'] = posts
	sql = 'select comm_id,post_id, name,content,timestamp from Comments join Users on Users.id = Comments.user_id'
	cursor.execute(sql)
	comments = cursor.fetchall()
	userdata['comments'] = comments

def getcommunityposts(userdata,id):
	sql = 'select name,content,time_stamp,p_id,photosrc,p_id from Users,Posts where community = %s and u_id = id and (u_id in (select u2_id from Friends where u1_id =%s) or u_id = %s)'%(id,session["userid"],session["userid"])
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
	sql3 = "select event_id from Attending where user_id='%s';"%(session['userid'])
	data['events'] = {}
	data['event_friends'] = {}
	cursor.execute(sql)
	events = cursor.fetchall()
	cursor.execute(sql2)
	event_friends = cursor.fetchall()
	cursor.execute(sql3)
	user_events = cursor.fetchall()
	data['user_events'] = [item[0] for item in user_events]
	for e in events:
		data['events'][int(e[0])] = e + tuple([[x[1] for x in event_friends if x[0] == e[0]]]) ;

def getuserdata(userdata):
	userdata['username'] = session['username']
	userdata['userid'] = session['userid']
	userdata['bio'] = session['bio']
	userdata['profile_picture'] = session['picture']

def getfrienddata(userdata):
	sql = "select name from Users where id=%s;"%(session['fid'])
	sql2 = "select bio from Users where id=%s;"%(session['fid'])
	sql3 = "select picture from Users where id=%s;"%(session['fid'])
	cursor.execute(sql)
	userdata['friendname'] = cursor.fetchone()[0]
	cursor.execute(sql2)
	userdata['fbio'] = cursor.fetchall()[0][0]
	cursor.execute(sql3)
	userdata['fprofile_picture'] = cursor.fetchall()[0][0]
	print(userdata['fprofile_picture'])

def getwalletdata(userdata):
	sql = "select wallet from Users where id = %s"%(session['userid'])
	cursor.execute(sql)
	wallet = cursor.fetchall()
	print(wallet[0][0])
	userdata['wallet'] = wallet[0]

def getuserfriends(userdata):
	# Overcomplicated query for extra marks ;)
	sql = "select distinct y.name,u2_id from Users join Friends on (Users.id = Friends.u1_id) join (select u2_id,name from Users join Friends on (Users.id = Friends.u2_id)) as y using(u2_id) where id = %s;"%(userdata['userid'])
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
	sql = "select M.*,Users.name from Users join (select m.m_id,m.From,m.Content,m.media,m.timestamp from Messages m where m.m_id in(select m1.m_id from Messages m1 where m1.To=%s and m1.From=%s UNION select m1.m_id from Messages m1 where m1.To=%s and m1.From=%s)) as M on M.From = Users.id;"%(session["userid"],session["fid"],session["fid"],session["userid"])
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

def gettransactions(userdata):
	sql = "select * from Transactions, Users where `from` =%s and `to`=id  order by timestamp desc;"%(session['userid'])
	cursor.execute(sql)
	transactions = cursor.fetchall()
	userdata['transactions'] = transactions

@app.route('/',methods=['GET'])
def home():
	# If user not logged in
	if not auth("/"): return redirect('/login')
	# Get all the details to display first and then render
	userdata = {}
	getuserdata(userdata)
	getuserfriends(userdata)
	getallusers(userdata)
	getfriendsposts(userdata)
	getfriendrequests(userdata)
	return render_template("./home.html",userdata = userdata, user = session['userid'])

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
		wallet = 1000
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
		sql2 = "Select * from Market,Payment,Users where id=user_id and item_id=i_id and user_id='%s';"%(session['userid'])
		cursor.execute(sql2)
		bought = cursor.fetchall()
		sql3 = "select wallet from Users where id='%s';"%(session['userid'])
		cursor.execute(sql3)
		wallet = cursor.fetchall()[0][0]
		return render_template('market.html',data=data, bought=bought, wallet = wallet)


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

	sql = "select price from Market where i_id = %s"%(id)
	cursor.execute(sql)
	money = cursor.fetchall()[0][0]
	print(money)
	sql2 = "call walletcheck('%s','%s','%s');"%(session['userid'],money,id)
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
		gettransactions(userdata)
		return render_template('./transaction.html',userdata=userdata)
	else:
		if not auth("/transaction"): return redirect('/login')
		f_id = request.form["friends"]
		amount = request.form["amount"]
		message = request.form["message"]
		sql = "call transactcheck('%s','%s','%s','%s');"%(session['userid'],amount,f_id,message)
		cursor.execute(sql)
		mydb.commit()
		return redirect("/transaction")

@app.route('/chats/<string:id>', methods=['GET'])
def chat_message(id):
	if not auth("/"): return redirect('/login')
	if int(id):
		session['fid'] = id
	userdata = {}
	messages = {}
	getmessages(messages)
	getuserdata(userdata)
	getfrienddata(userdata)
	getuserfriends(userdata)
	getallusers(userdata)
	getfriendsposts(userdata)
	getfriendrequests(userdata)
	return render_template('./chat.html',userdata=userdata, messages=messages)

@app.route('/chatstore', methods=['POST'])
def chatstore():
	if session['fid']:
		content = request.form['content']
		sql = "INSERT INTO `dbsproject`.`Messages` (`From`, `To`, `Content`, `timestamp`) VALUES ('%s', '%s', '%s', CURTIME());"%(session['userid'],session['fid'],content)
		cursor.execute(sql)
		mydb.commit()
		return redirect(url_for('chat_message', id=session['fid']))

@app.route('/Attend/<string:id>', methods=['GET'])
def Attend(id):
	print(id)
	print(session['userid'])
	sql = "INSERT INTO `dbsproject`.`Attending` VALUES ('%s', '%s');"%(id,session['userid'])
	cursor.execute(sql)
	mydb.commit()
	return redirect(url_for('events'))


@app.route('/community', methods=['GET'])
def viewcommunity():
	if not auth('/community'): return redirect('/login')
	userdata = {}
	getuserdata(userdata)
	getuserfriends(userdata)
	getallusers(userdata)
	getfriendrequests(userdata)
	sql = "select * from Community;"
	cursor.execute(sql)
	groups = cursor.fetchall()
	sql2 = "select * from Community, Belongs where community_id=c_id and user_id=(%s)"%(session['userid'])
	cursor.execute(sql2)
	communities = cursor.fetchall()
	print(communities)
	return render_template('viewcommunity.html',groups = groups, userdata = userdata, user = session['userid'], communities=communities)


@app.route('/groups/<string:id>', methods=['GET','POST'])
def groups(id):
	if request.method =='GET':
		sql = 'Select * from Belongs,Users where community_id='+id+' and user_id=id;'
		cursor.execute(sql)
		users = cursor.fetchall()
		print(users)
		c_users = [item[0] for item in users]
		if session['userid'] not in c_users:
			sql2 = "INSERT INTO `dbsproject`.`Belongs` VALUES('%s','%s');"%(session['userid'],id)
			cursor.execute(sql2)
			mydb.commit()
		session['currentgroup'] = id
		userdata = {}
		getuserdata(userdata)
		getcommunityposts(userdata,id)
		community = {}
		getcommunity(community,id)
		return render_template("groups.html", userdata = userdata, user = session['userid'], community = community, users=users)
	else:
		content = request.form['content']
		f = request.files['picture']
		if f:
			f.save('static/'+f.filename)
			sql = "INSERT INTO `dbsproject`.`Posts` (`u_id`, `content`, `time_stamp`,`photosrc`,`community`) VALUES ('%s', '%s', CURTIME(),'static/%s',%s);"%(session['userid'],content,f.filename,session['currentgroup'])
			cursor.execute(sql)
		else:
			sql = "INSERT INTO `dbsproject`.`Posts` (`u_id`, `content`, `time_stamp`,`community`) VALUES ('%s', '%s', CURTIME(),%s);"%(session['userid'],content,session['currentgroup'])
			cursor.execute(sql)
		mydb.commit()
		# Refresh, so that post is seen
		return redirect("/groups"+session['currentgroup'])

@app.route('/grouppost', methods=['POST'])
def grouppost():
		content = request.form['content']
		f = request.files['picture']
		if f:
			f.save('static/'+f.filename)
			sql = "INSERT INTO `dbsproject`.`Posts` (`u_id`, `content`, `time_stamp`,`photosrc`,`community`) VALUES ('%s', '%s', CURTIME(),'static/%s',%s);"%(session['userid'],content,f.filename,session['currentgroup'])
			cursor.execute(sql)
		else:
			sql = "INSERT INTO `dbsproject`.`Posts` (`u_id`, `content`, `time_stamp`,`community`) VALUES ('%s', '%s', CURTIME(),%s);"%(session['userid'],content,session['currentgroup'])
			cursor.execute(sql)
		mydb.commit()
		return redirect("/groups/"+session['currentgroup'])


@app.route('/addevent', methods=['POST'])
def addevent():
	description = request.form['description']
	location = request.form['location']
	f = request.files['media']
	if f:
		f.save('static/'+f.filename)
		sql = "INSERT INTO `dbsproject`.`Events` (`host`,`location`,`description`,mediasrc) VALUES('%s','%s','%s','static/%s')"%(session['userid'],location,description,f.filename)
		cursor.execute(sql)
	else:
		sql = "INSERT INTO `dbsproject`.`Events` (`host`,`location`,`description`) VALUES('%s','%s','%s')"%(session['userid'],location,description)
		cursor.execute(sql)
	mydb.commit()
	return redirect(url_for('events'))


@app.route('/music', methods=['GET'])
def music():
	userdata = {}
	getuserdata(userdata)
	getuserfriends(userdata)
	getallusers(userdata)
	getfriendsposts(userdata)
	getfriendrequests(userdata)
	sql = "select * from Music;"
	cursor.execute(sql)
	songs = cursor.fetchall()
	print(songs)
	sql2 = "select * from Music, Playlist where s_id=song_id and user_id='%s';"%(session['userid'])
	cursor.execute(sql2)
	playlist = cursor.fetchall()
	play = [item[0] for item in playlist]
	print(play)
	return render_template('music.html', songs=songs, userdata = userdata, user = session['userid'], playlist=playlist, play=play)

@app.route('/musicvideo/<string:id>', methods=['GET'])
def musicvideo(id):
	userdata = {}
	getuserdata(userdata)
	getuserfriends(userdata)
	getallusers(userdata)
	getfriendsposts(userdata)
	getfriendrequests(userdata)
	sql = "select * from Music where s_id='%s';"%(id)
	cursor.execute(sql)
	video = cursor.fetchall()
	sql2 = "select * from Music, Playlist where s_id=song_id and user_id='%s';"%(session['userid'])
	cursor.execute(sql2)
	playlist = cursor.fetchall()
	return render_template('musicplayer.html',video=video, userdata = userdata, user = session['userid'], playlist=playlist)

@app.route('/addtoplaylist/<string:s_id>', methods=['GET'])
def addtoplaylist(s_id):
	sql = "INSERT INTO `dbsproject`.`Playlist`VALUES('%s','%s')"%(session['userid'],s_id)
	cursor.execute(sql)
	mydb.commit()
	return redirect('/music')

@app.route('/addmarketitem', methods=['POST'])
def addmarketitem():
	title = request.form['title']
	description= request.form['description']
	price = request.form['price']
	f = request.files['picture']
	if f:
		f.save('static/'+f.filename)
		sql = "INSERT INTO `dbsproject`.`Market` (`title`,`description`,`price`,`seller`,`sold`) VALUES('%s','%s','%s',%s,0)"%(title,description,price,session['userid'])
		cursor.execute(sql)
	else:
		sql = "INSERT INTO `dbsproject`.`Market` (`title`,`description`,`price`,`seller`,`sold`) VALUES('%s','%s','%s',%s,0)"%(title,description,price,session['userid'])
		cursor.execute(sql)
	mydb.commit()
	return redirect('/market')

@app.route('/addcommunity', methods=['POST'])
def addcommunity():
	title = request.form['title']
	description= request.form['description']
	sql = "INSERT INTO `dbsproject`.`Community` (`name`,`description`) VALUES('%s','%s')"%(title,description)
	cursor.execute(sql)
	mydb.commit()
	return redirect('/community')

if __name__ == "__main__":
	app.run(port=3000, debug=False)
