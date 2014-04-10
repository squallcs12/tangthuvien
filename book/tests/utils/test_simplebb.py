'''
Created on Apr 10, 2014

@author: antipro
'''
from django.test import TestCase
import sure

from book.utils import simple_bb

class SimplebbTests(TestCase):
    def test_remove_bb_tags(self):
        text = """
        [SIZE][FONT][B][COLOR][U][I][URL][IMG]
        [/SIZE][/FONT][/B][/COLOR][/U][/I][/URL][/IMG]
        the text
        [/SIZE][/FONT][/B][/COLOR][/U][/I][/URL][/IMG]
        [SIZE][FONT][B][COLOR][U][I][URL][IMG]
        """

        text_without_bb = simple_bb(text)

        text_without_bb.strip().should.equal("the text")
