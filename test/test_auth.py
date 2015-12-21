# -*- coding: utf-8 -*-

import unittest
import os
from appd.download import Zone


class AuthFailureTest(unittest.TestCase):

    def setUp(self):
        self.base_url = 'https://download.appdynamics.com/onpremise/public/archives'
        self.zone = Zone(zone_id='on-premise',
                         username=os.environ.get('APPD_SSO_USERNAME'),
                         password=os.environ.get('APPD_SSO_PASSWORD'),
                         use_cookies=False)

    def test_auth_failure(self):
        bad_zone = Zone(zone_id='on-premise',
                         username=os.environ.get('APPD_SSO_USERNAME'),
                         password='xxxxxxxx',
                         use_cookies=False)
        self.assertRaises(RuntimeError, bad_zone.get_versions)


    def test_auth_success(self):
        self.zone.get_versions()
