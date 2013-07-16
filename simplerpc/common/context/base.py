# -*- coding: utf-8 -*-
'''
Simple RPC
Copyright (c) 2013, Joaquin G. Duo
'''
from simplerpc.common.log.Logger import Logger
from simplerpc.common.abstract.FrameworkObject import FrameworkObject
import inspect
from simplerpc.common.context.ContextWrapper import ContextWrapper

class context_singleton(object):
  '''
    Decorator that provides a single instance for the name argument provided
      I.e.: same name, same instance
      If the name differ, then a new instance is created
      It also wraps the context for a more friendly config access (as attrs)
  '''
  __instances = {}
  def __init__(self, class_):
    self.class_ = class_
  def __call__(self, name):
    if name not in self.__instances:
      self.__instances[name] = ContextWrapper(self.class_(name))
    return self.__instances[name]
  def get_current_contexts(self):
    return self.__instances

class ContextBase(FrameworkObject):
  '''
  Provides a global configuration storage.
  It can also have a per class configuration.
  Check :class:`simplerpc.common.base.SelfConfigBase.SelfConfigBase`
  '''
  def __init__(self, name):
    self.name = name
    self.__config = dict()
    self.set_config('log', Logger(name))
    self._loadInitConfig()

  def has_config(self, name, owner="global"):
    return self.__get_config_key(name, owner) in self.__config

  def get_config(self, name, owner="global"):
    if self.has_config(name, owner):
      return self.__config[self.__get_config_key(name, owner)]
    else:
      raise RuntimeWarning("No config '%s'." % self.__config_key_str(name, owner))

  def set_config(self, name, value, owner="global"):
    self.__config[self.__get_config_key(name, owner)] = value

  def __get_config_key(self, name, owner="global"):
    return (owner, name)

  def __config_key_str(self, name, owner="global"):
    if inspect.isclass(owner):
      string = "%s.%s" % (owner.__module__.__str__(),
                    owner.__name__)
    elif isinstance(owner, str):
      string = "%s" % owner
    else:#TODO: Print warning!!
      string = "%s" % owner
    string += '.%s' % name
    return string

  def _loadInitConfig(self):
    raise NotImplementedError('Implement on children')

def smokeTestModule():
  class Context(ContextBase):
    def _loadInitConfig(self):
      pass

  ctx = Context('smoke test')
  ctx.get_config('log').d('Testing')
  ctx.has_config('name')

if __name__ == "__main__":
  smokeTestModule()
