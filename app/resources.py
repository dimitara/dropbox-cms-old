# -*- coding: utf-8 -*-

import os
import markdown
from settings import LANGUAGES, SECTIONS
from flask import request, session, g, redirect, url_for, abort, render_template, flash, _app_ctx_stack, Blueprint, jsonify, Markup

cms = Blueprint('cms', __name__)
SECTIONS_KEYWORD = 'sections'
GALLERY_KEYWORD = 'gallery'

def escape(input):
    q1 = u'тАЬ'
    q2 = u'тАЭ'
    q3 = u'тАЩ'

    input = input.decode('utf8')
    input = input.replace(q1, '&quot;').replace(q2, '&quot;').replace(q3, '&apos;')

    return input

class Resources:
    def __init__(self, resource_location, settings_location):
        self.resource_location = resource_location
        self.settings_location = settings_location

        self.section_locations = resource_location + '/sections'
        self.pages_location = resource_location + '/pages'

        self.title = {}
        self.heading = {}
        self.logo = ''

        self.keywords = {}
        self.description = {}
        self.navigations = [];
        self.sections = {}
        self.analytics_tracking = ''

        self.pages = {}

        self.load_settings()
        self.load_navigations()
        #self.load_sections()
        self.load_pages()

    def load_sections(self):
        for key in SECTIONS:
            self.sections[key] = {}
            for locale in LANGUAGES:
                self.sections[key][locale] = {}
                content_file = open('%s/%s/%s/%s' % (self.section_locations, key, locale, 'content.txt'), 'r')

                self.sections[key][locale] = {}
                self.sections[key][locale]['content'] = Markup(markdown.markdown(escape(content_file.read())))

                content_file.close()

    def load_pages(self):
        self.pages = []
        self.pages.append(self.parse_page(self.pages_location, 'root'))


    def parse_page(self, folder, key):
        page = {
            'pages': [],
            'slug': key
        }
        
        if os.path.isdir(folder):
            self.parse_files(page, folder)

            items = os.listdir(folder)
            for item in items:
                if item in LANGUAGES: continue

                if item == SECTIONS_KEYWORD:
                    self.parse_sections(page, folder)
                    continue

                if item == GALLERY_KEYWORD:
                    self.parse_gallery(page, folder)
                    continue
                
                item_path = '%s/%s' % (folder, item)
                if os.path.isdir(item_path):
                    page['pages'].append(self.parse_page(item_path, item))
                
            return page
        else:
            return None    

    def parse_sections(self, page, folder):
        page['sections'] = []
        pass

    def parse_gallery(self, page, folder):
        pass

    def parse_files(self, page, folder):
        for lang in LANGUAGES:
            page[lang] = {}

            f_title = '%s/%s/%s' % (folder, lang, 'title.txt')
            f_nav = '%s/%s/%s' % (folder, lang, 'nav.txt')
            f_content = '%s/%s/%s' % (folder, lang, 'content.txt')

            if os.path.exists(f_title):
                title_file = open(f_title, 'r')
                page[lang]['title'] = escape(title_file.read())
                title_file.close()

            if os.path.exists(f_nav):
                nav_file = open(f_nav, 'r')
                page[lang]['nav'] = escape(nav_file.read())
                nav_file.close()

            if os.path.exists(f_content):
                content_file = open(f_content, 'r')
                page[lang]['content'] = escape(content_file.read())
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
            except Exception as e:
                print e
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

    def get_pages(self, locale):
        return self.pages

    def publish(self):
        #self.load_settings()
        self.load_navigations()
        self.load_pages()