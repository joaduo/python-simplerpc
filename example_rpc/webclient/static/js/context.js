/**
 * Simple RPC Javascript Library
 * Copyright (c) 2012-2013, LastSeal S.A.
 * This code is distributed under BSD 3-clause License. 
 * For details check the LICENSE file in the root of the project.
 */

(function (){
  
  function ModuleDefinition(){
    var contexts = {};
    
    function Context(){
     this.log = require('simplerpc/common/Logger')();
     this.config = {rpc_api_tests_path:'tests/rpc_api_methods_tests/drwebserver/rpc_api/'};
     this.global = {};
    }
    
    this.getContext = function (name){
      name = typeof name === 'undefined'? 'default': name;
      if(!(name in contexts)){
        contexts[name] = new Context();
      }
      return contexts[name];
    };

  }
  
  if(typeof module !== 'undefined' && this.module !== module)   //Register module on Nodejs
    module.exports = require('namespace').registerModuleNamespace(__filename,ModuleDefinition);
  else // Regiter on browser
    require('namespace').registerModuleNamespace(null,ModuleDefinition);

} )();
