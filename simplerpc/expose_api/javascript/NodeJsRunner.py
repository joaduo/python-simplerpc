# -*- coding: utf-8 -*-
'''
Simple RPC
Copyright (c) 2013, Joaquin G. Duo
'''
import os
from simplerpc.base.SimpleRpcLogicBase import SimpleRpcLogicBase
from simplerpc.expose_api.javascript.JsTranslateUtil import JsTranslateUtil
from simplerpc.common.FileManager import FileManager
import subprocess
import sys

class NodeJsRunner(SimpleRpcLogicBase):
  def __post_init__(self):
    self.js_util = JsTranslateUtil(self.context)
    self.file_manager = FileManager(self.context)

  def setNodePath(self):
    NODE_PATH = 'NODE_PATH'
    path = self.js_util._getProjectJsPath()
    if NODE_PATH not in os.environ:
      os.environ[NODE_PATH] = path
    else:
      os.environ[NODE_PATH] += ':' + path

  def __printJasmineErrors(self, file_path, ret_val, out, err):
    if ret_val:
      path = self.file_manager.formatFilePath(file_path)
      self.log.w('Error running jasmine test return value %s:\n%s' %
                 (ret_val, path))
      self.log.w('Stdout:\n%s' % out)
      self.log.w('Stderr:\%s' % err)
    return ret_val

  def runJasmineTest(self, file_path):
    argv = [self.context.jasmine_node_command, file_path, '--matchall',
            '--captureExceptions', '--noColor']
    return self.__printJasmineErrors(file_path, *self.runNodeJs(argv, pipe=True))


  def runNodeJs(self, argv=None, pipe=False):
    self.setNodePath()
    #node_command = 'node'
    if not argv:
      argv = sys.argv[1:]
    argv = [self.context.node_command] + argv
    if pipe:
      p = subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      return p.wait(), p.stdout.read(), p.stderr.read()
    else:
      p = subprocess.Popen(argv)
      return p.wait()

def smokeTestModule():
  from simplerpc.context.SimpleRpcContext import SimpleRpcContext
  context = SimpleRpcContext('run node.js')
  NodeJsRunner(context)#.runNodeJs()

if __name__ == "__main__":
  smokeTestModule()
