# -*- coding: utf-8 -*-
'''
Simple RPC
Copyright (c) 2013, Joaquin G. Duo
'''
from simplerpc.base.SimpleRpcLogicBase import SimpleRpcLogicBase
from simplerpc.common.path import joinPath, splitPath
import os
from simplerpc.common.FileManager import FileManager
import fnmatch

class TemplatesCollector(SimpleRpcLogicBase):
  '''
  Collects templates into stores in the repository
  to be used in the translation by the TranslationAstNode class.
  '''
  def __post_init__(self):
    self.file_manager = FileManager(self.context)

  def _getRepoPath(self, templates_set):
    return joinPath(os.path.dirname(__file__), templates_set)

  def _getTemplatesPaths(self, pattern, templates_set):
    for root, _, files in os.walk(self._getRepoPath(templates_set),
                                  followlinks=True):
      for basename in files:
        if fnmatch.fnmatch(basename, pattern):
          filename = os.path.join(root, basename)
          yield filename

  def _buildNamespace(self, file_path, templates_set):
      repo_split = splitPath(self._getRepoPath(templates_set))
      namespace, _ = os.path.splitext(file_path)
      namespace = splitPath(namespace)[len(repo_split):]
      return '.'.join(namespace)

  def collectBuiltIn(self, templates_set='javascript_templates'):
    templates = dict()
    for file_path in self._getTemplatesPaths('*.js', templates_set):
      namespace = self._buildNamespace(file_path, templates_set)
      template = self.file_manager.getTextFile(file_path)
      templates[namespace] = template
    return templates

def smokeTestModule():
  from simplerpc.context.SimpleRpcContext import SimpleRpcContext
  context = SimpleRpcContext('smoke test')
  templates = TemplatesCollector(context).collectBuiltIn()
  context.log(templates)

if __name__ == "__main__":
  smokeTestModule()
