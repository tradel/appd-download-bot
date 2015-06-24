# -*- coding: utf-8 -*-

import unittest
import os
from appd.download import Zone


class UrlParsingTest(unittest.TestCase):

    def setUp(self):
        self.version = '4.1.0.0'
        self.base_url = 'https://download.appdynamics.com/onpremise/public/archives'
        self.zone = Zone(zone_id='on-premise',
                         version=self.version,
                         username=os.environ.get('APPD_SSO_USERNAME'),
                         password=os.environ.get('APPD_SSO_PASSWORD'),
                         use_cookies=False)

    def test_controller_linux_64bit(self):
        url = self.zone.get_url('controller', 'linux', '64')
        self.assertEqual(url, '{0.base_url}/{0.version}/controller_64bit_linux-{0.version}.sh'.format(self))

    def test_controller_linux_32bit(self):
        url = self.zone.get_url('controller', 'linux', '32')
        self.assertEqual(url, '{0.base_url}/{0.version}/controller_32bit_linux-{0.version}.sh'.format(self))

    def test_controller_windows_64bit(self):
        url = self.zone.get_url('controller', 'windows', '64')
        self.assertEqual(url, '{0.base_url}/{0.version}/controller_64bit_windows-{0.version}.exe'.format(self))

    def test_controller_windows_32bit(self):
        url = self.zone.get_url('controller', 'windows', '32')
        self.assertEqual(url, '{0.base_url}/{0.version}/controller_32bit_windows-{0.version}.exe'.format(self))

    def test_controller_mac_64bit(self):
        url = self.zone.get_url('controller', 'mac', '64')
        self.assertEqual(url, '{0.base_url}/{0.version}/controller_64bit_mac-{0.version}.dmg'.format(self))

    def test_controller_mac_32bit(self):
        self.assertRaises(AssertionError, self.zone.get_url, 'controller', 'mac', '32')

