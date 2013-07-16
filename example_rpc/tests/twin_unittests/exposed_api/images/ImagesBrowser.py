# -*- coding: utf-8 -*-
'''
Simple RPC
Copyright (c) 2012-2013, LastSeal S.A.
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

if __name__ == "__main__":
  unittest.main()

