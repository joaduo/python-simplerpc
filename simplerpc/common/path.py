# -*- coding: utf-8 -*-
'''
Copyright (c) 2013, LastSeal S.A.
Copyright (c) 2011-2012, Joaquin G. Duo
All rights reserved.

This code is distributed under BSD 3-clause License.
For details check the LICENSE file in the root of the project.
'''

import os
import time
import sys

def realPath(path, retry=True):
  try:
    return os.path.realpath(path)
  except Exception as e:
    if retry:
      time.sleep(0.1)
      return os.path.realpath(path)
    else:
      raise e

def pathIsDir(path):
  return os.path.isdir(path)

def pathHead(path):
  return os.path.split(path)[0]

def pathExists(path, write=False):
  if write and os.access(path, os.W_OK):
    #self.context.log.debug("Exists: %r (writable)"%path)
    return True
  elif os.access(path, os.R_OK):
    #self.context.log.debug("Exists: %r  (readable)"%path)
    return True
  #self.context.log.debug("Doesn't exist: %r"%path)
  return False

def splitPath(path):
  return str(path).split(os.sep)

def joinPath(path, *path_list):
  if isinstance(path, list) or isinstance(path, tuple):
    path = os.sep.join(path)
  if len(path_list) != 0:
    for path_chunk in path_list:
      if isinstance(path_chunk, list) or isinstance(path_chunk, tuple):
        path = os.sep.join((path, joinPath(path_chunk)))
      else:
        path = os.sep.join((path, path_chunk))
#  if os.path.isabs(path):
#    path = os.path.realpath(path)
  return path


def formatPathPrint(path, line=None, error=False):
  if not line:
    line = 1
  path = os.path.realpath(path)
  return '  File "%s", line %d\n' % (path, line)

#  new_path_list = []
#  for path in path_list:
#    if isinstance(path,list):
#      path = joinPath(path)
#    new_path_list.append(path)
#  return os.sep.join(new_path_list)

#TODO: remove
#def conditionalPathJoin(str_list, split = False):
#  if split:
#    return str_list
#  else:
#    return os.sep.join(str_list)

def smokeTestModule():
  import logging
  logging.basicConfig()
  logging.debug(formatPathPrint(__file__, line=1))
  logging.debug(pathHead('/path/to/file'))
  logging.debug(pathIsDir('/home/jduo'))
  logging.debug(pathIsDir('/home/jduo/output.k3d'))

if __name__ == '__main__':
  smokeTestModule()

