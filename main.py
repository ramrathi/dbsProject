import os
import mysql.connector
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

mydb = mysql.connector.connect(
  host=os.getenv("localhost"),
  user=os.getenv("user"),
  passwd=os.getenv("passwd"),
  database=os.getenv("dbsproject")
)

cursor1 = mydb.cursor()
sql = "blah blah"
cursor1.execute(sql)
cursor1.commit() # if update
data = cursor1.fetchall() # if select

from flask import Flask, render_template
app = Flask(__name__)

@app.route('/',methods=['GET'])
def home():
	return render_template("./home.html")

@app.route('/login',methods=['GET','POST'])
def login():
	if request.method == 'POST':
		email = request.form["email"]
		password = request.form["password"]

		sql = "select * from users where email = %s and password = %s;"
		cursor.execute(sql)
		data = cursor.fetchall()
		if data == null:
			return render_template('./index.html',error = "Wrong email or password")
		else:
			# Set session variables to true
			return redirect('/')
	else:
		return render_template("./index.html")

@app.route('/register',methods=['GET'])
def register():
	return render_template("./register.html")

@app.route('/account',methods=['GET'])
def account():
	return render_template("./profile.html")


if __name__ == "__main__":
    app.run(port=3000, debug=True)