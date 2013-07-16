'''
Created on Mar 18, 2012

@author: jduo
'''

import sys
import inspect

mayor_version = sys.version[0]

def on_python_3():
  return mayor_version == '3'


def portable_getargspec(func):
  '''
    A tuple of four things is returned: (args, varargs, varkw, defaults).
    'args' is a list of the argument names.
    'args' will include keyword-only argument names.
    'varargs' and 'varkw' are the names of the * and ** arguments or None.
    'defaults' is an n-tuple of the default values of the last n arguments.

    Use the getfullargspec() API for Python-3000 code, as annotations
    and keyword arguments are supported. getargspec() will raise ValueError
    if the func has either annotations or keyword arguments.
  :param func:
  '''
  #TODO: change for something else?
  return inspect.getargspec(func)


def smokeTestModule():
  on_python_3()
  portable_getargspec(on_python_3)

if __name__ == '__main__':
  smokeTestModule()
