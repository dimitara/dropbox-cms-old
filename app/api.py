# -*- coding: utf-8 -*-

import os
import sys

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, Blueprint, jsonify
from resources import Resources
from settings import RESOURCES_PATH, SETTINGS_PATH

blueprint_api = Blueprint('api', __name__)
resource = Resources(RESOURCES_PATH, SETTINGS_PATH)

@blueprint_api.route('/api')
def home():
    global resource
    lang = request.args.get('l') or 'bg'
    print resource.get_navigations(lang)
    content = {
        "navigation": resource.get_navigations(lang),
        "pages": resource.get_pages(lang)
    }

    return jsonify(content)

@blueprint_api.route('/api/publish')
def publish():
    global resource

    resource.publish()

    return jsonify({'result': True})
