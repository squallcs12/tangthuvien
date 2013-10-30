'''
Created on Aug 6, 2013

@author: antipro
'''
from tangthuvien.templatetags import static_tags


class ClearTemplateJsCss(object):
    def process_request(self, request):
        static_tags.css_files = []
        static_tags.js_files = []
