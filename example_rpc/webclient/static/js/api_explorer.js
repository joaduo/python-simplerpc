

function printApiExplorer(rpc_class_namespace){
  var context = require('context').getContext();
  context.log.d('Below you can browse Javascript namespace.');
  require('namespace').printNamespace();
  var exposed_api = require(rpc_class_namespace)(context).getApiRoot();
  context.log.d('Below you can browse the exposed RPC api.');
  context.log.d(exposed_api)
  return exposed_api;
}


if(typeof module !== 'undefined' && this.module !== module && require.main === module){ //We are on Nodejs
  printApiExplorer('example_rpc/ExposedRpcApi');
}

