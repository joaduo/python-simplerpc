    this.${METHOD_NAME} = function (${ARGS} callback, error_callback){
      var cmd_string = '${RPC_METHOD}'; 
      var args = [${ARGS}];
      var kwargs = {};
      checkRequiredArgument({${KWARGS}}, '${METHOD_NAME}(${ARGS} callback, error_callback)');
      pushCommand(cmd_string, args, kwargs, callback, error_callback);    
    };