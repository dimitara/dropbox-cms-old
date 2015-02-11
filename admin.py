# -*- coding: utf-8 -*-
import os
import re
import db
from sqlite3 import dbapi2 as sqlite3
from flask import request, session, g, redirect, url_for, abort, render_template, flash, _app_ctx_stack, Blueprint
from dropbox.client import DropboxClient, DropboxOAuth2Flow
from settings import DATABASE, DROPBOX_APP_KEY, DROPBOX_APP_SECRET, LANGUAGES

admin = Blueprint('admin', __name__)

@admin.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        if username:
            db.add_user(username)
            session['user'] = username
            return redirect(url_for('admin.dashboard'))
        else:
            pass

    return render_template('admin/login.html', error=error)

@admin.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('/'))

@admin.route('/scaffold')
def scaffold():
    if 'user' not in session:
        return redirect(url_for('login'))

    generate_scaffold()
    return redirect(url_for('admin.dashboard'))

@admin.route('/sync')
def sync():
    if 'user' not in session:
        return redirect(url_for('login'))

    access_token = get_access_token()
    print(access_token)
    real_name = ''

    if access_token is not None:
        client = DropboxClient(access_token)
        gallery_items = client.metadata('/gallery')
        for idx, item in enumerate(gallery_items['contents']):
            if item['is_dir']:
                pass
            else:
                name = get_image_name(item['path'], '/gallery/')

                f, metadata = client.get_file_and_metadata(item['path'])

                make_dir('%s/%s' % (GAL_PATH, name))

                for lang in LANGUAGES:
                    make_dir('%s/%s/%s' % (GAL_PATH, name, lang))

                create_file('%s/%s.jpg' % (GAL_PATH, name), f.read())

                for lang in LANGUAGES:
                    create_file('%s/%s/%s/%s' % (GAL_PATH, name, lang, 'title.txt'), '')


    return redirect(url_for('admin.dashboard'))

@admin.route('/dropbox-auth-finish')
def dropbox_auth_finish():
    username = session.get('user')
    if username is None:
        abort(403)
    try:
        access_token, user_id, url_state = get_auth_flow().finish(request.args)
    except DropboxOAuth2Flow.BadRequestException as e:
        abort(400)
    except DropboxOAuth2Flow.BadStateException as e:
        abort(400)
    except DropboxOAuth2Flow.CsrfException as e:
        abort(403)
    except DropboxOAuth2Flow.NotApprovedException as e:
        flash('Not approved?  Why not, bro?')
        return redirect(url_for('/'))
    except DropboxOAuth2Flow.ProviderException as e:
        app.logger.exception("Auth error" + e)
        abort(403)

    db.update_token(access_token, username)

    return redirect(url_for('admin.dashboard'))

@admin.route('/dropbox-auth-start')
def dropbox_auth_start():
    if 'user' not in session:
        abort(403)
    return redirect(get_auth_flow().start())


@admin.route('/dropbox-unlink')
def dropbox_unlink():
    username = session.get('user')
    if username is None:
        abort(403)
    db = get_db()
    db.execute(
        'UPDATE users SET access_token = NULL WHERE username = ?', [username])
    db.commit()
    return redirect(url_for('home'))

@admin.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/')

    access_token = get_access_token()

    real_name = ''

    if access_token is not None:
        client = DropboxClient(access_token)
        account_info = client.account_info()
        real_name = account_info["display_name"]

    return render_template('admin/dashboard.html', real_name=real_name)

def get_auth_flow():
    redirect_uri = url_for('admin.dropbox_auth_finish', _external=True)
    return DropboxOAuth2Flow(DROPBOX_APP_KEY, DROPBOX_APP_SECRET, redirect_uri,
                             session, 'dropbox-auth-csrf-token')

def get_access_token():
    username = session.get('user')
    if username is None:
        return None

    return db.get_access_token(username)

def get_image_name(file_name, folder):
    file_name = file_name.replace(folder, '')

    insensitive_jpg_extension = re.compile(re.escape('.jpg'), re.IGNORECASE)
    file_name = insensitive_jpg_extension.sub('', file_name)

    return file_name

def make_dir(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

def create_file(file_name, content):
    out = open('%s' % file_name, 'wb')
    out.write(content)
    out.close()

def generate_scaffold():
    sections = ['team', 'partners', 'history', 'capacity', 'certification', 'breeds', 'contacts']

    make_dir('static/website')
    make_dir('static/website/gallery')
    make_dir('static/website/sections')

    for idx, section in enumerate(sections):
        dir_name = 'static/website/sections/%s-%s' % (idx, section)
        make_dir(dir_name)
        for lang in LANGUAGES:
            make_dir('%s/%s' % (dir_name, lang))
            create_file('%s/%s/%s' % (dir_name, lang, 'content.txt'), '')