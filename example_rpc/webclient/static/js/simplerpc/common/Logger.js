/**
 * Simple RPC Javascript Library
 * Copyright (c) 2012-2013, LastSeal S.A.
 * This code is distributed under BSD 3-clause License. 
 * For details check the LICENSE file in the root of the project.
 */

(function (){
  
  function ClassDefinition(n){
    var indent_level = 0;
    
    function printMsg(arguments){
      for(var index in arguments){
        console.log(arguments[index]);
      }
    }
    
    function defaultValue(default_value, value){
      return typeof value === 'undefined' ? default_value:default_value;
    }
    
    this.d = function (){printMsg(arguments);};
    this.i = function (){printMsg(arguments);};
    this.w = function (){printMsg(arguments);};
    this.e = function (){printMsg(arguments);};
    this.c = function (){printMsg(arguments);};

  }
  
  if(typeof module !== 'undefined' && this.module !== module)   //Register module on Nodejs
    module.exports = require('namespace').registerClassNamespace(__filename, ClassDefinition);
  else // Regiter on browser
    require('namespace').registerClassNamespace(null, ClassDefinition);

} )();
