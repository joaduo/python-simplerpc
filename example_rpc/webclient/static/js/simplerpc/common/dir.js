/**
 * Simple RPC Javascript Library
 * Copyright (c) 2012-2013, LastSeal S.A.
 * This code is distributed under BSD 3-clause License. 
 * For details check the LICENSE file in the root of the project.
 */

(function (){
  
  function ModuleDefinition(){

    this.dir = function (object){
      var object_attrs = [];
      for (var attr in object) {
          object_attrs.push(attr);
      }
      return object_attrs;
    };

  }
  

  if(typeof module !== 'undefined' && this.module !== module)   //Register module on Nodejs
    module.exports = require('namespace').registerModuleNamespace(__filename, ModuleDefinition);
  else // Register on browser
    require('namespace').registerModuleNamespace(null, ModuleDefinition);

} )();

