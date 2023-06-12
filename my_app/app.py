from flask import Flask, render_template, request, redirect, g
import sqlite3
import os

main_app = Flask(__name__)

# Function to get current database.
def get_db():
    db_name = "webappdb.db"
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, db_name)
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(db_path)
    return db

# Teardown function allows databse to be clsed after request.
@main_app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
        

# Executes database queries and returns result.
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    result = cur.fetchall()
    cur.close()
    get_db().commit()
    return (result[0] if result else None) if one else result

    
# Index functions redirects us to /register page
@main_app.route("/")
def index():
    return redirect('/register')


# Register page allows user to add a username and password
@main_app.route("/register")
def register():
    games = ["Poker", "Battleship", "Chess", "Pick-up Sticks"]
    return render_template("register.html", games=games)


# Submit checks if username is already in database return successful register page if user does not exist.
@main_app.route("/submit", methods=["POST"])
def submit():
    username = request.form.get('name')
    game = request.form.get('game')
    with main_app.app_context():
        try:
            query_db("INSERT INTO Users(username, game) VALUES(?,?)", (username, game))
            return render_template('register_success.html', username=username)
        except:
            return render_template('register_fail.html')
            


# Returns all registered users in html when POST is called an JSON when GET is called.
@main_app.route("/users", methods=['GET', 'POST'])
def users():
    cur = get_db().cursor()
    result = query_db("SELECT username, game FROM Users")
    if request.method == "POST":
        output=[]
        for user in result:
            output.append("User: Game")
            if len(user) > 0:
                output.append(f"{user[0]} : {user[1]}") 
        return render_template("users.html", users=output)
    elif request.method == "GET":
        output = {}
        for i, user in enumerate(result):
            output[i] = [user[0], user[1]]
        return output
    
    
        
    