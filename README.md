## Create a Virtual Environment using:
   python -m virtualenv dbsprojectenv

## Install Required Packages:
  pip install -r requirements.txt

## Create the database:
  mysql -u username -p < ./Extra_files/enti\(tit\)y_mysql_create.sql

## Create .env in the same directory and add
1. localhost='localhost'
2. database='dbsproject'
3. passwd='*your_password*'
4. user='*your_username*'

## Run the app
  python main.py
