from flask import Flask, render_template, request
from db import DB_PATH
import sqlite3

my_app = Flask(__name__)

def db_connections():
    connect = sqlite3.connect(DB_PATH)
    connect.row_factory = sqlite3.Row
    return connect

@my_app.route("/")
def hello_world():
    return render_template('home.html')

@my_app.route("/contact")
def contact_page():
    return render_template('contact.html')

@my_app.route("/form", methods = ['GET', 'POST'])
def form_page():
    
    name_flask = request.args.get('name_html')
    email_flask = request.args.get('email_html')
    mobile_flask = request.args.get('mobile_html')
    
    if name_flask and email_flask and mobile_flask:
        
        conn = db_connections()
        conn.execute(
            "INSERT INTO userdata (name, email, mobile) VALUES(?,?,?)", (name_flask, email_flask, mobile_flask)
            )
        conn.commit()
        conn.close()
        
         # return f"Hello {name_flask}, your EmailID is {email_flask} and Mobile Number is {mobile_flask}"
        return render_template("form.html", name = name_flask, email = email_flask, mobile = mobile_flask)
    
    return render_template('form.html')



