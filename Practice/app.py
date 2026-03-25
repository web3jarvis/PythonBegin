from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# db config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
        
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

with app.app_context():
    db.create_all()
        
@app.route("/", methods=['GET', 'POST'])
def home():
    users = User.query.all()
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        
        new_user = User(name=name, email=email)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for("home"))
    return render_template("home.html", users=users)

@app.route("/delete/<int:id>")
def delete(id):
    delete_user = User.query.get_or_404(id)
    
    db.session.delete(delete_user)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/update/<int:id>", methods=['GET', 'POST'])
def update(id):
    update_user = User.query.get_or_404(id)
    
    if request.method == "POST":
        update_user.name = request.form["name"]
        update_user.email = request.form["email"]
        
        db.session.commit()
        return redirect(url_for("home"))
    
    return render_template("update.html", users=update_user)
        
        
    
if __name__ == "__main__":
    app.run(debug=True)