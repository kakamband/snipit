from rest_framework.test import APITestCase
from main.models import Url
from main.api.views import shorten_url

from django.urls import reverse
import json


class SetUpClass(APITestCase):
    @classmethod
    def setUpTestData(cls):
        """
        this method sets up the data to be used across 
        multiple methods"""
        global url, valid_payload, invalid_payload

        url = Url.objects.create(
                                    long_url="https://nyior-clement.netlify.app/",
                                    shortcode="xxbb5t")
        valid_payload = {
                            "longUrl": "https://nyior-clement.netlify.app/",
                            "shortcode": "xxbb5"
                        }

        invalid_payload = {
                            "longUrl": "https://nyior-clement.netlify.app/"
                            }


class ShortenUrlView(SetUpClass):
    """ This tests the shorten url function"""               

    def test_view_returns_status_ok(self):
        """tests if view always return an ok response"""
        route = reverse("shorten-url")
        resp = self.client.post(route, valid_payload, format='json')
        resp2 = self.client.post(
                                    route, 
                                    invalid_payload, 
                                    format='json')

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp2.status_code, 200)

    def test_view_returns_shortcode(self):
        """tests if shortcode is in the response returned
        the goal is to test the functionality of creating custom
        urls. It also verifies that a user's custom short url is 
        atleast 4 chars long"""
        route = reverse("shorten-url")
        resp = self.client.post(route, valid_payload, format='json')

        self.assertEqual(resp.data, valid_payload)
        self.assertTrue(len(resp.data["shortcode"]) >= 4)

    def test_shortcode_isnot_null(self):
        """tests that the value of the shortcode returned is not null
        the goal is to tes the functionality of system generated 
        short urls. It also verifies that an autogenerated url
        is 6 chars long
        """
        route = reverse("shorten-url")
        resp = self.client.post(route, invalid_payload, format='json')

        self.assertTrue(resp.data["shortcode"] is not None)
        self.assertTrue(len(resp.data["shortcode"]) == 6)