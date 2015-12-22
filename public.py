# -*- coding: utf-8 -*-
import os
import sys

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, Blueprint, jsonify
from cms import CMS

public = Blueprint('public', __name__)
cms = CMS('static/resources/sections', 'static/resources/system/settings')

@public.route('/')
def home():
    global cms
    lang = request.args.get('l') or 'bg'
    
    content = {
        "title": cms.title[lang],
        "heading": cms.heading[lang],
        "keywords": cms.keywords[lang],
        "description": cms.description[lang],
        "navigation": cms.get_navigations(lang),
        "sections": cms.get_sections(lang),
        "analytics": cms.analytics_tracking
    }

    return render_template('public/index.html', content=content)
