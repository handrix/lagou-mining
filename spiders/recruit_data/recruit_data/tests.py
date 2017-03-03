# -*- coding:utf-8 -*-

import unittest
import os
import sys

class RecruiteSpiderTest(unittest.TestCase):
    def setUp(self):
        project_root = __file__.rsplit('/', 2)[0]
        os.chdir(project_root)
        self.client = os.path.join(os.path.dirname(sys.executable), 'scrapy')
        pass

    def lagou_test(self):
        os.system('{} crawl lagou -s DOWNLOAD_DELAY={}'.format(self.client, '1'))
        pass

if __name__ == '__main__':
    unittest.main()
