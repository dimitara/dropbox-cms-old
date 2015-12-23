import os
from sqlite3 import dbapi2 as sqlite3
from flask import _app_ctx_stack
from settings import DATABASE, APP_ROOT

def init_db(app):
    """Creates the database tables."""
    with app.app_context():
        db = get_db()
        with app.open_resource("schema.sql", mode="r") as f:
            db.cursor().executescript(f.read())
        db.commit()

def get_db():
    """
    Opens a new database connection if there is none yet for the current application context.
    """
    top = _app_ctx_stack.top
    if not hasattr(top, 'sqlite_db'):
        sqlite_db = sqlite3.connect(
            os.path.join(APP_ROOT, 'db', DATABASE))
        sqlite_db.row_factory = sqlite3.Row
        top.sqlite_db = sqlite_db

    return top.sqlite_db

def add_user(username):
    db = get_db()
    db.execute(
        'INSERT OR IGNORE INTO users (username) VALUES (?)', [username])
    db.commit()

def get_access_token(username):
    db = get_db()
    row = db.execute(
        'SELECT access_token FROM users WHERE username = ?', [username]).fetchone()
    if row is None:
        return None
    return row[0]

def update_token(access_token, username):
    db = get_db()
    data = [access_token, username]
    db.execute('UPDATE users SET access_token = ? WHERE username = ?', data)
    db.commit()