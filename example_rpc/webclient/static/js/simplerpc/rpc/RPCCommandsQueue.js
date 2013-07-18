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
      var requests_queue = {};
      var id_count = 0;

      this.push = function(cmd_string, args, kwargs, callback, error_callback){
        //Create json-rpc request
        var request = {
              jsonrpc:'2.0',
              method:cmd_string,
              params:[args,kwargs],
              id:id_count,
            };
        context.log.d('Pushing request: "'+request+'"');
        //Add it to the commands queue
        var request_data = {
            callback:callback,
            error_callback:error_callback,
            request:request,
        };
        //finally add it
        requests_queue[id_count] = request_data;
        id_count += 1;
      };

      this.pop = function(){
        var id_pop = id_count -1;
        var request_data = requests_queue[id_pop];
        delete requests_queue[id_pop];
        context.log.d('Popping request: '+ request_data.request);
      };
      
      function processRequestAnswer(request_data, answer){
        //extract request for smaller code
        var request = request_data.request;
        if(!answer.error){
          //call associated callback
          var callback = request_data.callback;
          if(callback){
            context.log.d('Calling request "'+ request +
                          '" callback: "' + 
                          RPCConnection.formatForLog(callback));
            callback(answer.result);
          }
          else{
            context.log.d('No callback for request "'+ request +
                          '" with id: '+ request.id);
          }
        }
        else{
          //There was an error, call the error_callback with data sent in 
          //the error (may be a message or something else)
          //call associated error_callback
          var error_callback = request_data.error_callback;
          if(error_callback){
            context.log.d('Calling request error_callback: ' + 
                RPCConnection.formatForLog(error_callback) + 
                'for command "'+ +'" ');
            context.log.d('Result was: "'+answer.result+'"');
            error_callback(answer.error);
          }
          else{
            context.log.d('No error_callback associated for request "'+
                request+ '". Result Error: "'+ answer.error +'"');
          }
        }        
      }
      
      function checkMissinAnswers(answers_ids){
        var missing_answers = [];
        //Iterate over queue request to check if one has no aswer
        for(var request_id in requests_queue){
          if(!request_id in answers_ids){
            missing_answers.push(request_id);
          }
        }
        //Report the problem
        if(missing_answers.length > 0){
          msg = 'There where '+missing_answers.length +'missing answers'
          context.log.e(msg)
          throw new Error(msg);
        }
      }
      
      function syncCallback(data){
        var answers = data.answers;
        var answers_ids = [];
        //Iterate over answers and match them with their ids
        for(var index in answers){
          var answer = answers[index];
          if(answer.id in requests_queue){
            //get request data to extract callback and error_callback 
            var request_data = requests_queue[answer.id];
            processRequestAnswer(request_data, answer);
          }
          else{
            var msg = 'Unexpected answer:'+answer
            context.log.e(msg);
            throw new Error(msg);
          }
          answers_ids.push(answer.id);
        }
        //Report about requests without answers
        checkMissinAnswers(answers_ids);
      }
      
      function errorCallback(error){
        context.log.e('Error while calling RPCConnection.syncRPC: ');
        context.log.d(error);
      }

      this.sync = function(){
        if(requests_queue.length == 0){
          context.log.d('No commands in queue. Nothing to do.');
        }
        //Send the ajax request through POST
        var requests = [];
        for(var rid in requests_queue){
          requests.push(requests_queue[rid].request);
        }
        var post_args = {'requests':JSON.stringify(requests)};
        RPCConnection.asyncGameServerRPC('/requests_queue/', '', post_args, 
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
