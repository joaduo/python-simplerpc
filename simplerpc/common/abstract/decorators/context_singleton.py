# -*- coding: utf-8 -*-
'''
Copyright (c) 2013, LastSeal S.A.
Copyright (c) 2011-2012, Joaquin G. Duo
All rights reserved.

This code is distributed under BSD 3-clause License.
For details check the LICENSE file in the root of the project.
'''


class context_singleton(object):
  '''
    Singleton pattern decorator.
    It provides a singleton for a determined class_ in a determined Context.
    So for each Context there will be only once instance of the decorated class.
  '''
  def __init__(self, class_):
    self.class_ = class_
  def __call__(self, context=None, *a, **ad):
    if context == None:
      msg = "You should always provide a context for class: %r" % self.class_.__class__.__name__
      raise RuntimeError(msg)
    if not context.has_config('singleton', self.class_):
      context.set_config('singleton', self.class_(context=context, *a, **ad), self.class_)
    return context.get_config('singleton', self.class_)

def smokeTestModule():
  from simplerpc.common.context.base import ContextBase
  class Context(ContextBase):
    def _loadInitConfig(self):
      pass
  ctx = Context('smoke test')
  @context_singleton
  class Example(object):
    def __init__(self, context):
      pass
  assert Example(ctx) == Example(ctx)



if __name__ == '__main__':
  smokeTestModule()
