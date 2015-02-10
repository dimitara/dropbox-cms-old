# -*- coding: utf-8 -*-
import os
import sys

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, Blueprint


public = Blueprint('public', __name__)

@public.route('/')
def home():
    website_name = u'Симента ООД'
    return render_template('public/index.html', website_name=website_name)
