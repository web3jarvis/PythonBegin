from flask import Flask, render_template, request

my_app = Flask(__name__)

@my_app.route("/", methods = ['GET'])
def home():
    return render_template("p_home.html")
    
# @my_app.route("/square/<number>")
# def square(number):
#     sq = int(number) * int(number)
#     return f"Square of {number} is {sq}"

@my_app.route("/p_form.html", methods = ['GET', 'POST'])
def form():
    
    message = None
    
    if request.method == "POST":
        name_f = request.form.get('name_h')
        email_f = request.form.get('email_h')
    
        message = f"Welcome {name_f}, your email is {email_f}"
        return render_template("p_form.html", msg = message)    
    
    return render_template("p_form.html")
    

