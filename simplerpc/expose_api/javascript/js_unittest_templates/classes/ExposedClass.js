
describe('${NAMESPACE}', function(){
  //Context and method solver
  var context = require('context').getContext('testing');
  var auto_sync = true;
  var exposed_rpc_api = require('${EXPOSED_RPC_API_CLASS}')(context, auto_sync);
  var methods = exposed_rpc_api.requireApi('${NAMESPACE}');
  ${METHODS}
})
