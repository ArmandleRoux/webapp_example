import sqlite3
import os
from flask import g
from app import return_app
    
main_app = return_app()

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
        
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    result = cur.fetchall()
    cur.close()
    get_db().commit()
    return (result[0] if result else None) if one else result
            