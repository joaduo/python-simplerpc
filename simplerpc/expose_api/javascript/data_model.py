# -*- coding: utf-8 -*-
'''
Simple RPC
Copyright (c) 2013, Joaquin G. Duo
'''
from simplerpc.base.SimpleRpcObject import SimpleRpcObject
import string

class TranslationAstNode(SimpleRpcObject):
  '''
  #TODO: document
  '''
  def __init__(self, template_namespace):
    '''

    :param parent: Parent of this node, None for root
    :param template_namespace: template name (with namespace)
    :param translation: translation dictionary for the node
    '''
    self.__template_namespace = template_namespace
    self.__translation = dict()
    #internal
    self._template = ''
    self.__children = dict()
    self.__children_order = []
    self.__parent = None

#  def setTemplate(self, template):
#    self._template = template

  def setParent(self, parent):
    self.__parent = parent

  def translate(self, name=None, value=None, **kwargs):
    '''
    Add a string to the translation dictionary or
    append child to this tree node

    :param name: name of the child (string)
    :param value: value (any TranslationAstNode or a str)
    '''
    if name:
      #String, add it to the dicionary
      if isinstance(value, basestring):
        self.__translation[name] = value
      #ist a children node
      elif name not in self.__children:
        self.__children_order.append(name)
        self.__children[name] = value
        if isinstance(value, TranslationAstNode):
          value.setParent(self)
      else:
        raise TypeError('Child %r already exists' % name)
    #iterate over keywords
    for name, v in kwargs.items():
      self.translate(name, v)


  def getString(self, templates):
    '''
    Get the string of all children with the given templates

    :param templates:
    '''

    translation = dict()
    for name in self.__children_order:
      value = self.__children[name]
      translation[name] = value.getString(templates)
    translation.update(self.__translation)
    template = self._getTemplate(templates)
    return string.Template(template).safe_substitute(translation)

  def _getTemplate(self, templates):
    namespace = self.__template_namespace
    if namespace in templates:
      return templates[namespace]
    elif self._template:
      return self._template
    else:
      raise TypeError('There is no template for such namespace: %r.' % namespace)


class AutoTemplateAstNode(TranslationAstNode):
  '''
  '''
  def __init__(self):
    TranslationAstNode.__init__(self, 'AUTO_TEMPLATE_AST_NODE')
    self._template = ' '

  def translate(self, name=None, value=None, **kwargs):
    '''
    Add a string to the translation dictionary or
    append child to this tree node.
    Also add to the template automatically

    :param name: name of the child (string)
    :param value: value (any TranslationAstNode or a str)
    '''
    if name:
      self._template += '\n${%s}' % name
      TranslationAstNode.translate(self, name, value)

    for name, v in kwargs.items():
      self.translate(name, v)

def smokeTestModule():
  root = TranslationAstNode(template_namespace='example')
  child = AutoTemplateAstNode()
  root.translate('child', child)
  #now we render it
  root = AutoTemplateAstNode()
  root.translate('child', child)
  root.getString(templates={})


if __name__ == "__main__":
  smokeTestModule()
