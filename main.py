import os
import mysql.connector
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# My fucking pip stopped working so now I can't install .env, can we just shift to yaml?
mydb = mysql.connector.connect(
  host="localhost",
  user="yourusername",
  passwd="yourpassword",
  database="dbsproject"
)


cursor = mysql.cursor()

# sql = "blah blah"
# cursor.execute(sql)
# cursor.commit() # if update
# data = cursor.fetchall() # if select


from flask import Flask, render_template
app = Flask(__name__)

@app.route('/home',methods=['GET'])
def home():
	return render_template("./index.html")

if __name__ == "__main__":
    app.run(port=3000, debug=True)