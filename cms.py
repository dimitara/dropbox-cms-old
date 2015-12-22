# -*- coding: utf-8 -*-

import markdown
from settings import LANGUAGES, SECTIONS
from flask import request, session, g, redirect, url_for, abort, render_template, flash, _app_ctx_stack, Blueprint, jsonify, Markup

cms = Blueprint('cms', __name__)

def escape(input):
    q1 = u'тАЬ'
    q2 = u'тАЭ'
    q3 = u'тАЩ'

    input = input.decode('utf8')
    input = input.replace(q1, '&quot;').replace(q2, '&quot;').replace(q3, '&apos;')

    return input

class CMS:
    def __init__(self, content_location, settings_location):
        self.content_location = content_location
        self.settings_location = settings_location

        self.title = {}
        self.heading = {}
        self.logo = ''

        self.keywords = {}
        self.description = {}
        self.navigations = [];
        self.sections = {}
        self.analytics_tracking = ''

        self.load_settings()
        self.load_navigations()
        self.load_sections()

    def load_sections(self):
        for key in SECTIONS:
            self.sections[key] = {}
            for locale in LANGUAGES:
                self.sections[key][locale] = {}
                content_file = open('%s/%s/%s/%s' % (self.content_location, key, locale, 'content.txt'), 'r')

                self.sections[key][locale] = {}
                self.sections[key][locale]['content'] = Markup(markdown.markdown(escape(content_file.read())))

                content_file.close()


    def load_settings(self):
        for lang in LANGUAGES:
            title_file = open('%s/%s/%s' % (self.settings_location, lang, 'title.txt'), 'r')
            self.title[lang] = escape(title_file.read())
            title_file.close()

            heading_file = open('%s/%s/%s' % (self.settings_location, lang, 'heading.txt'), 'r')
            self.heading[lang] = escape(heading_file.read())
            heading_file.close()

            description_file = open('%s/%s/%s' % (self.settings_location, lang, 'description.txt'), 'r')
            self.description[lang] = escape(description_file.read())
            description_file.close()

            keywords_file = open('%s/%s/%s' % (self.settings_location, lang, 'keywords.txt'), 'r')
            self.keywords[lang] = escape(keywords_file.read())
            keywords_file.close()

        analytics_file = open('%s/%s' % (self.settings_location, 'analytics.txt'), 'r')
        self.analytics_tracking = analytics_file.read()
        analytics_file.close()

    def load_navigations(self):
        i = 0
        for key in SECTIONS:
            i+=1
            nav = {}

            try:
                for locale in LANGUAGES:
                    nav_file = open('%s/%s/%s/%s' % (self.content_location, key, locale, 'nav.txt'), 'r')
                    nav[locale] = escape(nav_file.read())
                    nav['href'] = "#" + key
                    nav['index'] = i - 1

                    nav_file.close()

                self.navigations.append(nav)
            except:
                pass


    def get_navigations(self, locale):
        navs = []
        for key in self.navigations:
            navs.append({"index": key['index'], "href": key['href'], "caption": key[locale]})

        return navs

    def get_sections(self, locale):
        sections = {}

        for key in self.sections:
            sections[key] = {}
            sections[key]['content'] = self.sections[key][locale]['content']

        return sections