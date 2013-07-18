/**
 * Simple RPC Javascript Library
 * Copyright (c) 2012-2013, LastSeal S.A.
 * This code is distributed under BSD 3-clause License. 
 * For details check the LICENSE file in the root of the project.
 */

(function (){
  
  function ClassDefinition(context){
    
    var ConnectionManager = require('simplerpc/common/ConnectionManager')(context);
    
    function getUrlBase(){
      if(typeof module !== 'undefined' && this.module !== module){
        //On nodejs
        return {server:'localhost', port:8002}; //document.urlBase;
      }
      else{
        return {server:location.hostname, port:location.port};
      }
    }

    function getPublicServerUrlBase(){
      return getUrlBase();
    }

    function buildUrlGetArgs(args){
      var args_string = '?';
      for(var name in args){
        args_string += name +'='+ args[name] + '&';
      }
      return args_string;
    }

    function asyncRPCPost(path, post_args, callback, error_callback){
      //console.log('Calling asyncRPCPost at path:'+path+' with post args:'+post_args);
      asyncGameServerRPC(path, '', post_args, callback, error_callback);
    }

    function formatForLog(callback){
      return String(callback).slice(0,50);
    }
    
    this.formatForLog = function(callback){
      return formatForLog(callback);
    };

    this.asyncGameServerRPC = function(path, get_args, post_args, callback, error_callback){
      var url_base = getUrlBase();
      ConnectionManager.ajax(url_base.server, url_base.port, path, get_args, post_args, callback, error_callback);
    };

    this.syncPublicReadOnlyRPC = function(path, get_args, callback, error_callback){
      function callbackWrapper(result){
        if(typeof callback !== 'undefined'){
          callback(result.return_value);
        }
        else{
          context.log.d('No callback defined for public readonly RPC:"'+ path +'"');
        }
      }
      var url_base = getPublicServerUrlBase();
      path = '/public_readonly/' + path; 
      ConnectionManager.ajax(url_base.server, url_base.port, path, get_args, null, callbackWrapper, error_callback);
    };

  }
  
  if(typeof module !== 'undefined' && this.module !== module)   //Register module on Nodejs
    module.exports = require('namespace').registerClassNamespace(__filename, ClassDefinition);
  else // Regiter on browser
    require('namespace').registerClassNamespace(null, ClassDefinition);

} )();
