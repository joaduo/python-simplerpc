/**
 * Simple RPC Javascript Library
 * Copyright (c) 2012-2013, LastSeal S.A.
 * This code is distributed under BSD 3-clause License. 
 * For details check the LICENSE file in the root of the project.
 */

(function (){ //Anonymous function to avoid global namespace clogging
  
  function onNodeJs(){
    return typeof module !== 'undefined' && this.module !== module;
  }
  
  function namespace(){

    function __getRoot(){
      if(onNodeJs()){
        if(typeof GLOBAL.namespace_root == 'undefined'){
          GLOBAL.namespace_root = new Object();
        }
        return GLOBAL.namespace_root; 
      }
      else{
        if(typeof GLOBAL_namespace_root == 'undefined'){
          GLOBAL_namespace_root = new Object();
        }
        return GLOBAL_namespace_root;
      }
    };

    function appendNamespace(parent, namespace){
      if(typeof(parent[namespace]) == 'undefined'){
        parent[namespace] = new Object();
      }
      return parent[namespace];
    }
    
    function getWrappedClassContainer(class_, namespace) {
      return function () {
        //Call this function to get an Instance of the class at the required namespace. (passing construction arguments of the class; do not use the "new" keyword)
        var object = {}; 
        class_.apply(object, arguments);
        object.__proto__ = class_.prototype;
        return object;
      };
    }
    
    function namespaceToNamesList(namespace){
      return namespace.split('/');
    }
    
    function __latestLoadedScriptURL(){
      var scripts= document.getElementsByTagName('script');
      return scripts[scripts.length-1].src;
    }
    
    function autoCreateNamespace(namespace){
      if(namespace !== null){ //Probably on nodejs
        if(namespace.indexOf(__getScriptsRootURL()) >= 0){
          return namespace.slice(__getScriptsRootURL().length, namespace.length - '.js'.length);
        }
        else{
          return namespace;
        }
      }
      else{ //Probably on browser
        var module_url = __latestLoadedScriptURL();
        if(module_url.indexOf(__getScriptsRootURL()) >= 0){
          return module_url.slice(__getScriptsRootURL().length, module_url.length - '.js'.length);
        }
        else{
          throw new Error('Seems the script "'+module_url+'" does not share same URL root as this namespace.js script.');
        }
      }
    };
    
    var scripts_root_url = null;
    function __getScriptsRootURL(){
      if(onNodeJs()){
        return __filename.slice(0,__filename.length - 'namespace.js'.length);
      }
      else{ //On browser, then it must be initialized
        if(scripts_root_url != null){
          return scripts_root_url;
        }
        else{
          throw new Error('scripts_root_url was not initialized');
        }        
      }
    }
    
    this.initScriptsRootURL = function(){
      scripts_root_url = __latestLoadedScriptURL().replace('namespace.js', '');
    };
    
    function registerNamespace(namespace, container, force){
      force = typeof force === 'undefined' ? false : force;
      var names = namespaceToNamesList(namespace); 
      var parent = __getRoot();
      for ( var index = 0; index < names.length-1; index++) {
        parent = appendNamespace(parent, names[index]);
      }
      
      if(typeof parent[names[index]] === 'undefined'){
        //finally register the container in the namespace if it was not defined
        parent[names[index]] = container;
      }
      else{
        if(force){
          //register the container in the namespace overwriting previous value
          console.log('Overwriting namespace:'+namespace+'. Old object was:');
          console.log(parent[names[index]]);
          console.log('New object is:');
          console.log(container);
          parent[names[index]] = container;
        }
        else{
          throw new Error('Trying to overwrite existing namespace="'+namespace+'"');
        }
      }
    }
    
    this.registerClassNamespace = function (namespace, class_definition, force){
      namespace = autoCreateNamespace(namespace);
      class_definition.__namespace__ = namespace;
      var container = getWrappedClassContainer(class_definition, namespace);
      registerNamespace(namespace, container, force);
      return container;
    };
    
    this.registerModuleNamespace = function (namespace, module_definition, force){
      namespace = autoCreateNamespace(namespace);
      module_definition.__namespace__ = namespace;
      var container = new module_definition();
      registerNamespace(namespace, container, force);
      return container;
    };
    
    this.getModule = function (namespace, caller){
      var names = null;
      if(namespace.indexOf('./') >= 0){
        if(typeof caller.__namespace__ === 'undefined'){
          throw new Error('Beware, requiring relative modules only works on class\'s or module\'s definition function. Caller namespace attribute seems not defined.');
        }
        //get the namespace of the caller of require
        names = namespaceToNamesList(caller.__namespace__);
        //create names root for relative loading
        names = names.slice(0,names.length-1);
        //append relatives names
        names = names.concat(namespaceToNamesList(namespace.slice(2,namespace.length))); 
      }
      else{
        names = namespaceToNamesList(namespace); 
      }
            
      //console.log('Getting "'+ namespace+'".');
      var parent = __getRoot();
      for (var index in names) {
        parent = parent[names[index]];
        if(typeof parent === 'undefined')
          throw new Error('Namespace "'+names[index]+'" at position '+index+' for namespace "'+namespace+'" doesn\'t exist. (sometimes this means a circular dependency)');
      }
      return parent;
    };
 
    this.printNamespace = function (){
      console.log(__getRoot());
    };
  }

  if(onNodeJs()){
    module.exports = new namespace();
  }
  else{
    GLOBAL_namespace_module = new namespace();
    GLOBAL_namespace_module.initScriptsRootURL();
  }
  
})();

if(!(typeof module !== 'undefined' && this.module !== module)){ //We are outside nodejs
  if(typeof require != 'undefined'){//require may be defined on a Browser, warn the developer about it.
    console.log('"require" global variable is defined. It will be replaced to mimic node.js behavior.');
    console.log('Old "require" was:');
    console.log(require);
  }
  
  require = function (namespace){
    if(namespace == 'namespace'){
      return GLOBAL_namespace_module;
    }
    else{
      var caller = arguments.callee.caller;
      return GLOBAL_namespace_module.getModule(namespace, caller);
    }
  };
}

