/**
 * Simple RPC Javascript Library
 * Copyright (c) 2012-2013, LastSeal S.A.
 * This code is distributed under BSD 3-clause License. 
 * For details check the LICENSE file in the root of the project.
 */

(function (){
  
  function ClassDefinition(context){
    var current_branch = ['root'];
    var tests_results = {};
    var test_count = 0;
    
    this.appendTest = function (test_name){
      var test_number = test_count;
      tests_results[test_number] = {'test_name':current_branch.join('.')+'.'+test_name,'success':false,'message':null,};
      test_count += 1;
      return test_number;
    };
    
    this.endTest = function(test_number, success, message){
      tests_results[test_number].success = success;
      tests_results[test_number].message = message;
      console.log('Ending test_number='+test_number+' with result success='+success+' and message="'+message+'".');
    };
    
    this.enterBranch = function (branch_name){
      current_branch.push(branch_name);
    };
    
    this.leaveBranch = function (){
      current_branch.pop();
    };
    
    this.successIfArgumentsForCallback = function (test_number, expected_arguments){
      var self = this;
      function CallbackFunction(){
        var message = '';
        var success = true;
        //Test of length and arguments are all equal
        if(expected_arguments.length == arguments.length){
          for(var arg_index in expected_arguments){
            if(expected_arguments[arg_index] !== arguments[arg_index]){
              success = false;
            }
          }
        }
        else{
          success = false;
        }
        
        //Set message acording to test result
        if(success){
          message = 'Callback arguments as expected.';
        }
        else{
          message = 'Callback expected arguments "'+expected_arguments+'", instead got "'+arguments+'"';
        }
        //Submit result
        self.endTest(test_number, success, message);
      }
      return CallbackFunction;
    };
    
    this.failureIfCalled = function (test_number){
      var self = this;
      function CallbackFunction(){
        var success = false;
        var  message = 'Called failureIfCalled.';
        //Submit result
        self.endTest(test_number, success, message);
      }
      return CallbackFunction;
    };
    
    this.successIfCalled = function (test_number){
      var self = this;
      function CallbackFunction(){
        var success = true;
        var  message = 'Called successIfCalled.';
        //Submit result
        self.endTest(test_number, success, message);
      }
      return CallbackFunction;
    };
    
  }
  
  if(typeof module !== 'undefined' && this.module !== module)   //Register module on Nodejs
    module.exports = require('namespace').registerClassNamespace(__filename, ClassDefinition);
  else // Register on browser
    require('namespace').registerClassNamespace(null, ClassDefinition);

} )();
