# -*- coding: utf-8 -*-
import os
import sys

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, Blueprint
from cms import CMS

public = Blueprint('public', __name__)

@public.route('/')
def home():
    cms = CMS('static/resources/', 'website/settings')

    website_title = cms.title['bg']
    website_heading = cms.heading['bg']

    return render_template('public/index.html', website_title=website_title, website_heading=website_heading)
