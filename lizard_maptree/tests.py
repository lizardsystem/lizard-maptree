# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client


class IntegrationTest(TestCase):
    fixtures = ['lizard_maptree_test',]

    def test_homepage(self):
        c = Client()
        url = '/'
        response = c.get(url)
        self.assertEquals(response.status_code, 200)

    def test_category(self):
        c = Client()
        url = reverse('lizard_maptree.homepage',
                      kwargs={'root_slug': 'root'})
        response = c.get(url)
        self.assertEquals(response.status_code, 200)
