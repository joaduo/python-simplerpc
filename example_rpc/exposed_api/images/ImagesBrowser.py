# -*- coding: utf-8 -*-
'''
Simple RPC
Copyright (c) 2012-2013, LastSeal S.A.
'''
from simplerpc.expose_api.base.QueueCommandBase import QueueCommandBase

class ImagesBrowser(QueueCommandBase):
  '''
  #TODO: document Class
  '''
  def getImagesList(self):
    ''' #TODO: document method'''
    images = {}
    for img_id in range(20):
      images[img_id] = dict(name='Image%03d'%img_id, 
                            desc='Image %s made by John Doe'%img_id, 
                            url='static/images/Image%03d.jpg'%img_id)
    return images

  def getImage(self, image_id):
    pass

  def getSomethingElse(self, arg1, arg2, arg3):
    pass

if __name__ == "__main__":
  from simplerpc.testing.exposed_api.ExposedModuleAutotester import ExposedModuleAutotester
#  ExposedModuleAutotester().createJsUnitTest(overwrite=False)
  ExposedModuleAutotester().autoTest()
