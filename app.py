from flask import Flask,render_template,make_response,flash
import flask
from flask.globals import request
#from models.Users import User
from flask import Flask,g, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
import bcrypt
from flask_login import LoginManager
from functools import wraps

app = Flask(__name__)
app.secret_key = "testing"
app.config['MONGO_DBNAME'] = 'test'
app.config['MONGO_URI'] = "mongodb://localhost:27017/test"
mongo = PyMongo(app)



@app.route('/')
def index():
    email = ''
    if 'email' in session:
        email  = session['email']
    return render_template('home.html',email=email)




@app.route("/user/login", methods=["POST", "GET"])
def login():
    if "email" in session:
        return redirect(url_for("index"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        curr_user = mongo.db.Users.find_one({"email": email})
        if curr_user: 
            email_val = curr_user['email']
            passwordcheck = curr_user['password']
            
            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                session["email"] = email_val
                return redirect(url_for('index'))
            else:
                if "email" in session:
                    return redirect(url_for("index"))
                message = 'Wfasdfrong password'
                flash(message)
                return render_template('signup.html', message="fsdfsdf")
        else:
            flash('Email not found')
            return render_template('signup.html')
    return render_template('signup.html')



@app.route('/user/register', methods = ["GET", "POST"])
def register():
    if "email" in session:
        return redirect(url_for("index"))

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password1 = request.form.get("password")
        password2 = request.form.get("Confirm")
        users = mongo.db.Users
        curr_user = users.find_one({"email": email})

        if curr_user:
            flash('This email already exists in database')
            return render_template('signup.html')

        if password1 != password2:
            message = 'Passwords should match!'
            flash(message)
            return render_template('signup.html')
        else:
            hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
            user_input = {'name': name, 'email': email, 'password': hashed}
            users.insert_one(user_input)
            user_data = users.find_one({"email": email})
            new_email = user_data['email']
            return render_template('signup.html')
    return render_template('signup.html')
    
    
@app.route('/user/signup', methods = ["GET", "POST"])
def signup():
    return  render_template('signup.html')

@app.route("/user/logout", methods=["POST", "GET"])
def logout():
    if "email" in session:
        session.pop("email", None)
    return redirect(url_for("index"))