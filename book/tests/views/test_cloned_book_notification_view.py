'''
Created on Apr 10, 2014

@author: eastagile
'''
from django.core.urlresolvers import reverse
from django.test import Client
from django.test import TestCase
import sure

class IndexViewTest(TestCase):

    def setUp(self):
        # Every view test needs a Client
        self.client = Client()

    def test_simulate_thread_view(self):
        response = self.client.get(reverse("test_cloned_book_notification", kwargs={"thread_id": 10}))
        response.status_code.should.equal(200)

    def test_cloned_book_js_notification(self):
        url = reverse("cloned_book_notification", kwargs={"thread_id": 10})
        url[-3:].should.equal(".js")

        response = self.client.get(url)
        response.status_code.should.equal(200)
        response['content-type'].should.equal("application/javascript")
