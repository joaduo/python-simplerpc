# -*- coding: utf-8 -*-
'''
Simple RPC
Copyright (c) 2013, Joaquin G. Duo
'''
import sys

do_print = True
def printSmoke(msg, *args):
    if do_print:
        sys.stdout.write(str(msg))
        if len(args):
            sys.stdout.write(', '.join([''] + [str(a) for a in args]))
        sys.stdout.write('\n')

def smokeTestModule():
    printSmoke('msg')
    printSmoke('msg', 1, 2, [])

if __name__ == "__main__":
    smokeTestModule()
