/**
 * Simple RPC Javascript Library
 * Copyright (c) 2012-2013, LastSeal S.A.
 * This code is distributed under BSD 3-clause License. 
 * For details check the LICENSE file in the root of the project.
 */

(function (){
  
  function ClassDefinition(context){

    function buildUrlGetArgs(args){
      args_string = '?';
      count = 0;
      for(name in args){
        args_string += name +'='+ args[name] + '&';
        count += 1;
      }
      if(count)
        return args_string;
      else
        return '';
    }

    function formatForLog(callback){
      text = String(callback);
      if(text.length > 50)
        return '"'+String(callback).slice(0,50)+ ' ..."';
      else
        return '"'+String(callback).slice(0,50)+ '"';
    }

    function onNodejs(){
      //TODO: review this, taken from http://stackoverflow.com/questions/4224606/how-to-check-whether-a-script-is-running-under-node-js
      return typeof module !== 'undefined' && module.exports && this.module !== module;
    }

    function ajaxJquery(complete_url, post_args, callback, error_callback){
      if(typeof post_args != 'undefined' && post_args != null){
        console.log('Sending arguments via POST to:'+ complete_url);
        $.ajax({ type: 'POST',  dataType: 'json',
                 data: post_args,
                 url: complete_url, success: callback, error: error_callback 
        });
      }
      else{
        $.ajax({ type: 'GET',dataType: 'json',
                 url: complete_url, success: callback, error: error_callback 
        });
      }
    }

    function ajaxNodeJs(server, port, url, post_args, callback, error_callback){
      if(typeof post_args !== 'undefined' && post_args != null){
        ajaxNodeJsPost(server, port, url, post_args, callback, error_callback);
      }
      else{
        console.log('No GET method for Nodejs');
      }
    }

    function ajaxNodeJsPost(server, port, url, post_args, callback, error_callback){
      //We need this to build our post string
      var querystring = require('querystring');
      var http = require('http');

      // Build the post string from an object
      var post_data = querystring.stringify(post_args);
      //var post_data = JSON.stringify(post_args);

      // An object of options to indicate where to post to
      var post_options = {
          host: server,
          port: port,
          path: url,
          method: 'POST',
          headers: {
              'Content-Type': 'application/x-www-form-urlencoded',
              'Content-Length': post_data.length
          }
      };
      
      var resFunction = function(res) {
        var responseBuffer = '';
        var onDataFunction = function (chunk) {
          responseBuffer += chunk;
        };
        
        var onEndFunction = function (){
          //querystring.parse(responseBuffer)
          callback(JSON.parse(responseBuffer));
        };
        
        res.setEncoding('utf8');
        res.on('data', onDataFunction);
        res.on('end', onEndFunction);
      };

      // Set up the request
      var post_req = http.request(post_options, resFunction);

      // post the data
      post_req.write(post_data);
      post_req.end();
    }
    
    this.ajax = function (server, port, url, get_args, post_args, callback, error_callback){
      complete_url = 'http://' + server + ':'+ port + url + buildUrlGetArgs(get_args);
      url = url + buildUrlGetArgs(get_args);
      console.log('Connecting RPC API: '+complete_url);
      
      var successFunction = function(result) {
        // call callback function 
        if(typeof callback !== 'undefined' && callback != null) {
          console.log('Calling callback ' + formatForLog(callback)+' for url: ' + complete_url);
          callback(result);                
        }
        else{
          console.log('No success callback for url: ' + complete_url);
        }
      };
      
      var errorFunction = function(result) {
        console.log('Error for url: ' + complete_url);
        //call the error_callback if existent
        if( typeof error_callback !== 'undefined' && error_callback != null) {
          console.log('Calling error_callback '+ formatForLog(error_callback)+'.');
          error_callback(result);                
        }
        else{
          console.log('No error callback defined.');
          console.log('Result is:');
          console.log(result);
        }
      };

      if(onNodejs()){ //we are on Node.js
        ajaxNodeJs(server, port, url,  post_args, successFunction, errorFunction);
      }
      else{ //we are on a browser with jquery
        ajaxJquery(complete_url, post_args, successFunction, errorFunction);
      }
    };    

  }
  
  if(typeof module !== 'undefined' && this.module !== module)   //Register module on Nodejs
    module.exports = require('namespace').registerClassNamespace(__filename, ClassDefinition);
  else // Regiter on browser
    require('namespace').registerClassNamespace(null, ClassDefinition);

} )();
