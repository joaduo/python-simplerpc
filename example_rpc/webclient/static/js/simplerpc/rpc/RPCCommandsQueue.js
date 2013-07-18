/**
 * Simple RPC Javascript Library
 * Copyright (c) 2012-2013, LastSeal S.A.
 * This code is distributed under BSD 3-clause License. 
 * For details check the LICENSE file in the root of the project.
 */

(function (){
  
  function ClassDefinition(context){
    
    var RPCConnection = require('./RPCConnection')(context);

    function RPCCommandsQueue(){
      var commands_queue = [];
      var callbacks_queue = [];
      var error_callbacks = [];

      this.push = function(cmd_string, args, kwargs, callback, error_callback){
        //var cmd = [cmd_string,args,kwargs];
        var cmd = {
              jsonrpc:'2.0',
              method:cmd_string,
              params:[args,kwargs],
              id:commands_queue.length,
            };
        context.log.d('Pushing command: "'+cmd+'"');
        commands_queue.push(cmd);
        callbacks_queue.push(callback);
        error_callbacks.push(error_callback);
      };

      this.pop = function(){
        context.log.d('Popping cmd: '+ commands_queue.pop());
        callbacks_queue.pop();
        error_callbacks.pop();
      };

      function emptyArray(array){
        array.splice(0,array.length);
      }
      
      function syncCallback(data){
        var commands_results = data['results'];
        //Check if length match (same amount of commands sent and received)
        if (!commands_results.length == commands_queue.length){ 
          //Real error, answer should be of same length
          context.log.d('Receiving different amount of results ('+ 
                        commands_results.length +') for sent commands ('+ 
                        commands_queue.length +')');  
        }
        else if(commands_queue.length == 0){
          var msg = 'There were no commands. Then there sholdn\'t be any RPC.'
          throw new Error(msg);
        }
        else{
          for ( var index = 0; index < commands_results.length; index++) {
            //extract result and associated callbacks from arrays
            var cmd_result = commands_results[index];
            var callback = callbacks_queue[index];
            var error_callback = error_callbacks[index];
            //if there was no error for the command
            if(typeof cmd_result.error == 'undefined'){
              //call associated callback
              if(typeof callback !== 'undefined'){
                context.log.d('Calling command "'+ commands_queue[index][0] +
                              '" at index '+ index+' command callback "' + 
                              RPCConnection.formatForLog(callback));
                //callback(cmd_result['return_value']);
                callback(cmd_result.result);
              }
              else{
                context.log.d('No callback for command "'+
                              commands_queue[index][0] +'" at index: '+ index);
              }
            }
            else{ 
              //There was an error, call the error_callback with data sent in 
              //the error (may be a message or something else)
              //call associated error_callback
              if(typeof error_callback !== 'undefined'){
                context.log.d('Calling command error_callback ' + 
                    RPCConnection.formatForLog(error_callback) + 'for command "'+
                    commands_queue[index][0] +'" id '+ index );
                context.log.d(cmd_result);
                error_callback(cmd_result.error);
              }
              else{
                context.log.d('Error for RPC Command"'+ 
                    commands_queue[index][0] +'" number '+ index +
                    ' in the batch. No error_callback associated. Result Error: "'+ 
                    cmd_result.error +'"');
              }
            }
          }
        }
      }
      
      function errorCallback(error){
        context.log.e('Error while calling RPCConnection.syncRPC: ');
        context.log.d(error);
      }

      this.sync = function(){
        if(commands_queue.length == 0){
          context.log.d('No commands in queue. Nothing to do.');
        }
        //Send the ajax request through POST
        var post_args = {'cmds':JSON.stringify(commands_queue)};
        RPCConnection.asyncGameServerRPC('/commands_queue/', '', post_args, 
                                         syncCallback, errorCallback );
      };  

    }

    function RPCQueues(){
      var queues = new Object();
      var current_queue = new RPCCommandsQueue();
      var current_queue_number = 0;
      
      this.push = function (cmd_string, args, kwargs, callback, error_callback){
        current_queue.push(cmd_string, args, kwargs, callback, error_callback);
      };
      
      this.pop = function (){
        current_queue.pop();
      };
      
      this.sync = function (){
        queues[current_queue_number] = current_queue;
        current_queue = new RPCCommandsQueue();
        current_queue_number += 1;
        queues[current_queue_number-1].sync();
        //TODO: delete queue once it was synched
        //must create a getSyncCallBack(callback_at_end) in RPCCommandsQueue
        //pass function to sync that deletes the queue
      };
    }
    
    function getCommandsQueue(){
      var global_name = 'RPCCommandsQueue.rpc_commands_queue';
      if(!(global_name in context.global)){
        context.global[global_name] = new RPCQueues();
      }
      return context.global[global_name];
    }

    this.push = function(cmd_string, args, kwargs, callback, error_callback){
      getCommandsQueue().push(cmd_string, args, kwargs, callback, error_callback);
    };

    this.pop = function(){
      getCommandsQueue().pop();
    };

    this.sync = function(){
      //Send the ajax request through POST
      getCommandsQueue().sync();
    };
  }
  
  if(typeof module !== 'undefined' && this.module !== module)   //Register module on Nodejs
    module.exports = require('namespace').registerClassNamespace(__filename, ClassDefinition);
  else // Register on browser
    require('namespace').registerClassNamespace(null, ClassDefinition);

} )();
