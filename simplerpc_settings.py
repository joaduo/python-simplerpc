# -*- coding: utf-8 -*-
'''
Simple RPC
Copyright (c) 2013, Joaquin G. Duo
'''
from simplerpc.context.SimpleRpcSettings import SimpleRpcSettings
from simplerpc.common.path import joinPath
import example_rpc
from example_rpc import exposed_api

class Settings(SimpleRpcSettings):
    #determines the project path and all relative modules in this package
    project_package = example_rpc
    #we need to know where modules are for automating translation
    exposed_roots = [exposed_api]
    #if relative, its relative to the project package path
    js_path = './webclient/static/js'
    #Where the exposed rpc api class is stored
    js_rpc_file = joinPath(example_rpc.__name__, 'ExposedRpcApi.js')
    #set the node command
    node_command = 'node'
    #set the jasmine-node command
    jasmine_node_command = '/home/jduo/.programs/nodejs/lib/node_modules/jasmine-node/bin/jasmine-node'
