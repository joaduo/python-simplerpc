# -*- coding: utf-8 -*-
'''
Simple RPC
Copyright (c) 2013, Joaquin G. Duo
'''
from unittest.case import TestCase
from simplerpc.testing.exposed_api.base import ExposedTestBase
import unittest

class ImagesBrowser(ExposedTestBase, TestCase):
    '''
    #TODO: document Class
    '''
    def test_getImagesList(self):
        tested_instance = self._getTestedClass()()
        images = tested_instance.getImagesList()
        self.assert_(isinstance(images, dict))

#  def test_deleteImage(self):
#    pass

if __name__ == "__main__":
    unittest.main()
