# -*- coding: utf-8 -*-
import os
import re
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, _app_ctx_stack
from dropbox.client import DropboxClient, DropboxOAuth2Flow

SECRET_KEY = 'some-key'

# configuration
DEBUG = True

# create our little application :)
flask_app = Flask(__name__)
flask_app.config.from_object(__name__)
flask_app.config.from_envvar('FLASKR_SETTINGS', silent=True)

#from db import init_db
#from app.public import public
from app import api
#from admin import admin

#app.register_blueprint(public)
#app.register_blueprint(admin)
flask_app.register_blueprint(api.blueprint_api)

def main():
    flask_app.run()

if __name__ == '__main__':
#    init_db(app)
    main()
