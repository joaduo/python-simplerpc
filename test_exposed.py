#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Simple RPC
Copyright (c) 2013, Joaquin G. Duo
'''
from simplerpc.context.SimpleRpcContext import SimpleRpcContext
from simplerpc.testing.exposed_api.TestExposedModule import TestExposedModule
import argparse
import os
import logging

class TestExposed(object):
  '''
  Test a module given its path in the command line
  '''
  def run(self, argv=None):
    #get command's arguments parser and parse them
    parser = self.getArgsParser()
    args = parser.parse_args(argv)
    #set log level
    context = SimpleRpcContext('test exposed')
    if args.debug:
      context.log.setLevel(logging.DEBUG)
    #If path exists then run tests
    if os.path.exists(args.module_path):
      TestExposedModule(context).testModule(args.module_path)
    else:
      #does not exist, then print help
      parser.print_help()
      context.log.w('Module file does not exist: %r' % args.module_path)

  def getArgsParser(self):
    parser = argparse.ArgumentParser(description='Simple RPC exposed module tester.')
    help = 'specify the path to the module to be tested'
    parser.add_argument('module_path', action='store', help=help)
    help = 'Enable debug output.'
    parser.add_argument('--debug', action='store_true', help=help)
    return parser

def testExposed():
  TestExposed().run()

if __name__ == "__main__":
  testExposed()
