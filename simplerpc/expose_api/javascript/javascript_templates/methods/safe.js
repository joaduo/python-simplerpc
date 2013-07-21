    this.${METHOD_NAME} = function (${ARGS} callback, error_callback){
      var cmd_url = '${RPC_METHOD}';
      var kwargs = {${KWARGS}};
      checkRequiredArgument(kwargs, '${METHOD_NAME}(${ARGS} callback, error_callback)');
      syncPublicReadOnlyRPC(cmd_url, kwargs, callback, error_callback); 
    };