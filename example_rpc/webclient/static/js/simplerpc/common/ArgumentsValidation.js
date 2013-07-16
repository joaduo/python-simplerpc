/**
 * Simple RPC Javascript Library
 * Copyright (c) 2012-2013, LastSeal S.A.
 * This code is distributed under BSD 3-clause License. 
 * For details check the LICENSE file in the root of the project.
 */

(function (){
  
  function ClassDefinition(context){

    this.mandatory = function (value){
      if(typeof value == 'undefined')
        throw new Error('Undefined value for argument');
    };
    
    function defaultValue(default_value, value){
      return typeof value === 'undefined' ? default_value:default_value;
    }
  }
  
  if(typeof module !== 'undefined' && this.module !== module)   //Register module on Nodejs
    module.exports = require('namespace').registerClassNamespace(__filename, ClassDefinition);
  else // Regiter on browser
    require('namespace').registerClassNamespace(null, ClassDefinition);

} )();
