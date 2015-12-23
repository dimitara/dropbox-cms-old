# -*- coding: utf-8 -*-
import os
import sys

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, Blueprint, jsonify
from resources import Resources

public = Blueprint('public', __name__)
resource = Resources('static/resources', 'static/resources/system/settings')

@public.route('/')
def home():
    global resource
    lang = request.args.get('l') or 'bg'
    
    content = {
        "title": resource.title[lang],
        "heading": resource.heading[lang],
        "keywords": resource.keywords[lang],
        "description": resource.description[lang],
        "navigation": resource.get_navigations(lang),
        "sections": resource.get_sections(lang),
        "analytics": resource.analytics_tracking
    }

    return render_template('public/index.html', content=content)
