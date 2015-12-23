# -*- coding: utf-8 -*-
import os
import re
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, _app_ctx_stack
from dropbox.client import DropboxClient, DropboxOAuth2Flow

from app import public
from app import api

# configuration
DEBUG = True

# create flask app
flask_app = Flask(__name__)
flask_app.config.from_object(__name__)
flask_app.config.from_envvar('FLASKR_SETTINGS', silent=True)

# register blueprints to enable their routes
flask_app.register_blueprint(public.public_api)
flask_app.register_blueprint(api.blueprint_api)

def main():
    flask_app.run()

if __name__ == '__main__':
    main()
