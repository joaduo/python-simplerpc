# -*- coding: utf-8 -*-
'''
Copyright (c) 2011-2013, Joaquin G. Duo
Copyright (c) 2013, LastSeal S.A.
All rights reserved.

This code is distributed under BSD 3-clause License.
For details check the LICENSE file in the root of the project.
'''
from simplerpc.common.python3 import portable_getargspec
import traceback
import inspect
import sys

class PostInitStrategyBase(object):
  '''
    Adds the "__post_init__" capabilities to a class.
    Arguments received on "__post_init__" should always be passed as keywords,
      if not a TypeError exception will be Raised.
    There is no need to declare arguments as keywords but you need to provide
      them as keywords in the class initialization.
    This class is not meant to be inherited by concrete class, but by
      superclasses.
    Classes inheriting this class must call the _initChildren method in order
      to call all __post_init__ methods.
  '''
  def __init__(self, context):
    pass

  def _initChildren(self, args, kwargs):
    '''
    Gets the list of "__pre_init__" and "__post_init__" method for this class.
      Then calls the method in this this order
          __post_init__ (Eldest class in hierarchy)
        __post_init__
      __post_init__  (Concrete class in hierarchy)
      This way each concrete class can make a call before all initializations or after

    '''
    if len(args) > 0:
      raise TypeError('You should provide all "__post_init__" arguments as keywords.')
    # get the list of __post_init__ from lower classes to upper
    posts = []
    self.__getInitLists(self.__class__, posts, set())
    #call the list of __post_init__ (reverse to its discovery)
    self.__callInits(list(reversed(posts)), kwargs)

  def __callInits(self, funcs, kwargs):
    # Iterate functions and pass existing arguments.
    for class_, func in funcs:
      args = portable_getargspec(func)[0]
      #filter those arguments that this __post_init__ receives
      func_kwargs = dict(filter(lambda x: x[0] in args, kwargs.items()))
      try:
        #call the __post_init__ function
        func(self, **func_kwargs)
      except TypeError as error:
        # Extract the traceback of the exception
        tb_list = traceback.extract_tb(sys.exc_info()[2])
        # File where the error occurred
        error_file = self.__cleanFile(tb_list[-1][0])
        # if the error was calling func, then report accordingly.
        if error_file == self.__cleanFile(__file__):
          # The problems is calling func.
          # Get this traceback
          tb_list = traceback.extract_stack()
          # Create proper message to report the __post_init__ location.
          new_message = self.__reportLocalError(tb_list, class_, func, error)
        else:
          # The problem is not calling func.
          # Format the message so that the location is not lost in the report.
          new_message = self.__reportOutsideError(tb_list, class_, error)
        raise TypeError(new_message)

  def __cleanFile(self, file_name):
    #Get rid of .pyc if there.
    if file_name.endswith('.pyc'):
      return file_name[:-1]
    return file_name

  def __reportOutsideError(self, tb_list, class_, error):
    #Create a report of an error outside this file when one calling
    #__post_init__ method
    tb_list = traceback.format_list(tb_list)
    msg = '\nTraceback: \n'
    msg += ''.join(tb_list)
    msg += '%s' % error.message
    return msg

  def __reportLocalError(self, tb_list, class_, func, error):
    #Create a report of an error inside this file when one calling
    #__post_init__ method. (probably some argumenst typerror)
    tb_list = traceback.format_list(tb_list[:-3])
    msg = '\nTraceback: \n'
    msg += ''.join(tb_list)
    msg += '%s' % error.message
    # create traceback friendly report
    filename = inspect.getsourcefile(func)
    lines, lineno = inspect.getsourcelines(func)
    line = lines[0]
    name = func.__name__
    extracted_list = [(filename, lineno, name, line)]
    # Print the report
    func_hint = ''.join(traceback.format_list(extracted_list))
    msg += '\n\n%s' % (func_hint)
    msg += '      Remember that %r \n      only accepts keywords arguments in' \
                  ' the constructor.' % class_
    return msg

  def __getInitLists(self, class_, posts, already_added):
    #Visit the inheritance line to gather all the __post_init__ methods
    if class_ == PostInitStrategyBase:
      #Its this class we can stop recursion
      return
    #Is a subclass, the check if __post_init__exists
    if issubclass(class_, PostInitStrategyBase):
      if hasattr(class_, '__post_init__') and class_.__post_init__ not in already_added:
        #__post_init__ exists and we haven't add it yet
        posts.append((class_, class_.__post_init__))
        #remember it
        already_added.add(class_.__post_init__)
      #visit superclasses
      self.__getInitLists(class_.__base__, posts, already_added)
    else:
      #We end up in a superclass that is not this class. Consider it an error
      raise TypeError('InitStrategyBase should be on the main inheritance line.')


def smokeTestModule():
  class ExtendedBase(PostInitStrategyBase):
    def __post_init__(self, value, value1, test1 = 1, tat1 = 20):
      self.post_init_var1 = value1

  class ConcreteClass(ExtendedBase):
    def __post_init__(self, value, too, test = 1, tat = 20):
      self.post_init_var = value

  from simplerpc.context.SimpleRpcContext import SimpleRpcContext
  ctx = SimpleRpcContext('smoke test')

  cc = ConcreteClass(context = ctx)
  cc._initChildren([], dict(context = ctx, too = 2, something = 2312, value1 = 231, other_value = 20, value = 100, test = 2))
  ctx.log((cc.post_init_var, cc.post_init_var1))

if __name__ == '__main__':
  smokeTestModule()



