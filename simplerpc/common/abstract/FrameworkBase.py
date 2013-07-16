# -*- coding: utf-8 -*-
'''
Copyright (c) 2013, LastSeal S.A.
Copyright (c) 2011-2012, Joaquin G. Duo
All rights reserved.

This code is distributed under BSD 3-clause License.
For details check the LICENSE file in the root of the project.
'''
from simplerpc.common.abstract.SelfConfigBase import SelfConfigBase
from simplerpc.common.abstract.PostInitStrategyBase import PostInitStrategyBase


class FrameworkBase(PostInitStrategyBase, SelfConfigBase):
  def __init__(self, context, *a, **ad):
    SelfConfigBase.__init__(self, context=context)
    PostInitStrategyBase.__init__(self, context=context)
    PostInitStrategyBase._initChildren(self, a, ad)

def smokeTestModule():
  class ExtendedBase(FrameworkBase):
    def __post_init__(self, value):
      self.log('Post init abstract')
      self.post_init_var = value

  class Foo(object):
    pass

  #class ConcreteClass(Foo, ExtendedBase):
  class ConcreteClass(ExtendedBase, Foo):
    def __post_init__(self, value):
      self.log('Post init concrete')
      self.post_init_var = value

  from simplerpc.common.context.base import ContextBase
  class Context(ContextBase):
    def _loadInitConfig(self):
      pass

  ctx = Context('smoke test')
  FrameworkBase(context=ctx)
  ConcreteClass(context=ctx, value=1)

if __name__ == '__main__':
  smokeTestModule()

