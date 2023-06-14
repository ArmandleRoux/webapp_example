from flask import Flask, render_template, request, redirect, g, session
from flask_session import Session
import sqlite3
import os
from .db_manager import query_db
from hashlib import sha512

main_app = Flask(__name__)

main_app.config['SESSION_PERMANENT'] = False
main_app.config['SESSION_TYPE'] = 'filesystem'

Session(main_app)

# Function to get current database
def get_db():
    db_name = 'webappdb.db'
    # Get path to database
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, db_name)
    # define db equal to g module's database attribute if attribute
    # does not exist db will be equal to None
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(db_path)
    return db


# Teardown function allows databse to be closed after request.
@main_app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@main_app.route('/')
def index():
    if not session.get('name'):
        return redirect('/login')
    return redirect('/home')


# Register page allows user to add username and sport
@main_app.route("/register")
def register():
    return render_template('register.html')
    

@main_app.route("/login")
def login():
    return render_template('login.html')

@main_app.route("/logout")
def logout():
    session['name'] = None
    return redirect('/login')


@main_app.route('/home')
def home_page():
    username = session.get('name')
    return render_template('sign_in_home.html', username=username)


@main_app.route('/submitlogin', methods=["POST"])
def submit_login():
    username = request.form.get('name')
    password = request.form.get('password')
    password = sha512(password.encode('utf-8')).hexdigest()
    with main_app.app_context():
        result = query_db(get_db(), "SELECT password FROM USERS WHERE username=?", [username], True)
        print(password)
        print(result)
        if result and result[0] == password:       
            session['name'] = username    
            return redirect("/home")
        return render_template('login_fail.html', message="Username in unavailable!")


# Submit checks if username is already in database and return corresponding page.
@main_app.route('/submitregister', methods=["POST"])
def submit_register():
    username = request.form.get('name')
    password = request.form.get('password')
    confirm_pw = request.form.get('conf_pw')
    if password != confirm_pw:
        return render_template('register_fail.html', message="Passwords not matching!")
    password = sha512(password.encode('utf-8')).hexdigest()
    with main_app.app_context():
        try:
            query_db(get_db(), "INSERT INTO Users(username, password) VALUES(?,?)", (username, password))
            return render_template('sign_in_home.html', message= "Register Login", username=username)
        except:
            return render_template('register_fail.html', message="Username in unavailable!")
        

@main_app.route('/users', methods=["POST", "GET"])
def users():
    result = query_db(get_db(), "SELECT * FROM Users")
    if request.method == "POST":
        output = []
        output.append("Users")
        for user in result:
            output.append(f"{user}")
        return render_template('users.html', users=output)
    elif request.method == "GET":
        output = {}
        for i, user in enumerate(result):
            output[i] = [user[0], user[1]]
        return output
    
    
@main_app.route('/edit_user_data')
def edit_user_data():
    username = session['name']
    result = query_db(get_db(), "SELECT birth_date, colour FROM Users WHERE username=?", tuple(username), True)
    birth_date = result[0]
    colour = result[1]
    return render_template('add_user_data.html')
    
    
if __name__ == '__main__':
    main_app.run(debug=True)