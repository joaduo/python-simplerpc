# -*- coding: utf-8 -*-
'''
Simple RPC
Copyright (c) 2013, Joaquin G. Duo
'''
from simplerpc.expose_api.base.ExposedBase import ExposedBase
from simplerpc.expose_api.decorators import expose

class CrudBase(ExposedBase):
  '''
  Inherit from this class to implement API interfaces with the CRUD verbs.
  This should make your program more RESTFul like. (still not HATEOAS, that
  is something you should implement)
  Implement the create, read, update and delete methods without need to
  decorate them. This class will add needed decorators automatically.
  '''
  def __getattribute__(self, name):
    dec_map = {'create':expose,
               'read':expose.safe,
               'update':expose.idempotent,
               'delete':expose.idempotent}
    if name in dec_map:
      method = ExposedBase.__getattribute__(self, name)
      if not callable(method):
        msg = 'Attribute %s of %s should be callable' % (method, self)
        raise TypeError(msg)
      return dec_map[name](method)
    else:
      return ExposedBase.__getattribute__(self, name)


def smokeTestModule():
  from simplerpc.common.log.printSmoke import printSmoke
  class ExampleCrud(CrudBase):
    def create(self, arg1, arg2):
      pass
    def delete(self):
      pass
    def read(self):
      pass
  example = ExampleCrud()
  printSmoke(example.create)
  printSmoke(example.exposedMethods(expose.idempotent))
  printSmoke(example.exposedMethods(expose.safe))
  printSmoke(example.exposedMethods(expose))
  try:
    class ExampleCrud(CrudBase):
      update = None
    example = ExampleCrud()
    example.update
    raise Exception()
  except TypeError:
    pass

if __name__ == "__main__":
  smokeTestModule()
