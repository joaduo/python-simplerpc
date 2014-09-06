# -*- coding: utf-8 -*-
'''
Simple RPC
Copyright (c) 2012-2013, LastSeal S.A.
'''
from simplerpc.base.SimpleRpcLogicBase import SimpleRpcLogicBase
import os
from simplerpc.common.path import formatPathPrint
import inspect

class FileManager(SimpleRpcLogicBase):
    '''
    Class to manage File.
     -reading writing
     -making directories
     -checking paths
    '''
    def makedirs(self, path):
        if not (os.path.exists(path) and os.path.isdir(path)):
            os.makedirs(path)
        else:
            self.log.d('Ignoring %s' % path)

    def getTextFile(self, file_path):
        fr = open(file_path, 'r')
        text = fr.read()
        fr.close()
        return text

    def saveTextFile(self, file_path, content, overwrite=False):
        self.log.d('Writing %r with overwrite %s' % (file_path, overwrite))
        if not os.path.exists(file_path) or overwrite:
            target_file = open(file_path, 'w')
            target_file.write(content)
            target_file.close()
        else:
            self.log.w('Could not write over existing file %r' % file_path)

    def formatFilePath(self, file_path, line=1):
        return formatPathPrint(file_path, line)

    def formatClassFilePath(self, class_):
        file_path = inspect.getsourcefile(class_)
        _, line = inspect.getsourcelines(class_)
        path = self.formatFilePath(file_path, line)
        return path

def smokeTestModule():
    from simplerpc.context.SimpleRpcContext import SimpleRpcContext
    context = SimpleRpcContext('smoke test')
    fm = FileManager(context)
    text = 'this file shouldn t exist'
    file_path = __file__ + '.tmp'
    fm.saveTextFile(file_path, text)
    assert text == fm.getTextFile(file_path)
    import os
    if os.path.exists(file_path):
        os.remove(file_path)

if __name__ == '__main__':
    smokeTestModule()
