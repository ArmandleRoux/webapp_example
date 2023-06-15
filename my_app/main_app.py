from flask import render_template, request, redirect, session, Blueprint
from flask_login import login_required, current_user, login_user, logout_user
from . import db
from .models import User
from hashlib import sha512


main_app = Blueprint('main_app', __name__)

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
    logout_user()
    session['name'] = None
    return redirect('/login')


@main_app.route('/home')
@login_required
def home_page():
    username = session.get('name')
    return render_template('sign_in_home.html', username=username)


@main_app.route('/submitlogin', methods=["POST"])
def submit_login():
    username = request.form.get('name')
    password = request.form.get('password')
    password = sha512(password.encode('utf-8')).hexdigest()
    print(username)
    user = User.query.filter_by(username=username).first()
    print(user)
    if user and user.password == password:     
        session['name'] = username
        login_user(user) 
        return redirect("/home")
    return render_template('login_fail.html', message="Login has failed!")


# Submit checks if username is already in database and return corresponding page.
@main_app.route('/submitregister', methods=["POST"])
def submit_register():
    username = request.form.get('name')
    password = request.form.get('password')
    confirm_pw = request.form.get('conf_pw')
    if password != confirm_pw or not auth_password(password):
        return render_template('register_fail.html', message="Please note that your password entries have to match and should be more than 8 characters.")
    password = sha512(password.encode('utf-8')).hexdigest()
    try:
        new_user = User(username=username, password=password, fav_colour=None, birth_date=None)
        db.session.add(new_user)
        db.session.commit()
    except:
        return render_template('register_fail.html', message="Username in unavailable!")
    new_user = User.query.filter_by(username = username).first()
    login_user(new_user)
    return render_template('sign_in_home.html', message= "Register Success", username=username)
        
        

@main_app.route('/users', methods=["POST", "GET"])
@login_required
def users():
    result = User.query.order_by(User.username).all()
    print(result)
    if request.method == "POST":
        output = []
        output.append("Users")
        for user in result:
            output.append(f"{user.username}")
        return render_template('users.html', users=output)
    elif request.method == "GET":
        output = {}
        for i, user in enumerate(result):
            output[i] = [user.username]
        return output
    
    
@main_app.route('/edit_user_data')
@login_required
def edit_user_data():
    username = session['name']
    user = User.query.filter_by(username = username).first()
    colour = user.fav_colour
    return render_template('add_user_data.html', colour=colour)
    
    
def auth_password(password):
    if 8 <= len(password) <= 24:
        return True
    return False
        
    
    
if __name__ == '__main__':
    main_app.run(debug=True)