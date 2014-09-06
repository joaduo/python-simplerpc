# -*- coding: utf-8 -*-
'''
Simple RPC
Copyright (c) 2013, Joaquin G. Duo
'''
from simplerpc.base.SimpleRpcObject import SimpleRpcObject
import string

class TranslationAstNode(SimpleRpcObject):
    '''
    This class is used when translating Python API into other language.
    When introspecting existing packages, modules and classes a AST tree will be
    created.
    Given a template dictionary, this class can translate itself into a string
    via the getString method.
    '''
    def __init__(self, template_namespace):
        '''
        :param template_namespace: template name to look up in the templates dict
        '''
        self.__template_namespace = template_namespace
        self.__translation = dict()
        #internal
        self._template = ''
        self.__children = dict()
        self.__children_order = []
        self.__parent = None

    def setParent(self, parent):
        '''
        When adding a child node we need a method to set its parent.
        :param parent: parent TranslationAstNode node
        '''
        self.__parent = parent

    def translate(self, name=None, value=None, **kwargs):
        '''
        Add a string to the translation dictionary or append child if it's a tree
        node
        :param name: name of the child (string)
        :param value: value (any TranslationAstNode or a str)
        '''
        if name:
            #String, add it to the dicionary
            if isinstance(value, basestring):
                self.__translation[name] = value
            #ist a children node
            elif isinstance(value, TranslationAstNode):
                if name not in self.__children:
                    self.__children_order.append(name)
                    self.__children[name] = value
                    value.setParent(self)
                else:
                    raise TypeError('Child %r already exists' % name)
            else:
                msg = 'Value type not TranslationAstNode or basetring. Value: %s' % value
                raise TypeError(msg)
        #iterate over keywords
        for name, v in kwargs.items():
            self.translate(name, v)


    def getString(self, templates):
        '''
        Get the string of all children with the given templates

        :param templates: dictionary of templates
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
    This TranslationAstNode enables to add other node automatically without need
    to have the name in a existing template.
    The template is created on the fly in the order names and values are created.
    '''
    def __init__(self):
        TranslationAstNode.__init__(self, 'AUTO_TEMPLATE_AST_NODE')
        self._template = ' '

    def translate(self, name=None, value=None, **kwargs):
        '''
        Add a string to the translation dictionary or
        append child to this tree node.
        Also adds to the template automatically so that the value appears on the
        translation.

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
