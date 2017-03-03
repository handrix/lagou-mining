# -*- coding: utf-8 -*-

from __future__ import absolute_import
import unittest
import os
import sys


class ProxiesTests(unittest.TestCase):
    def setUp(self):
        project_root = __file__.rsplit('/', 2)[0]
        os.chdir(project_root)
        self.client = os.path.join(os.path.dirname(sys.executable), 'scrapy')
        pass

    def test_xicidaili(self):
        os.system('{} crawl xicidaili'.format(self.client))
        pass

    def test_youdaili(self):
        """
        该代理不可靠
        :return:
        """
        os.system('{} crawl youdaili'.format(self.client))
        pass

    def test_kuaidaili(self):
        os.system('{} crawl kuaidaili'.format(self.client))
        pass

    pass
