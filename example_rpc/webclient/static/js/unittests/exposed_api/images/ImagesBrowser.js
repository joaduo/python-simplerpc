
describe('images/ImagesBrowser', function(){
  //Context and method solver
  var context = require('context').getContext('testing');
  var auto_sync = true;
  var exposed_rpc_api = require('example_rpc/ExposedRpcApi.js')(context, auto_sync);
  var methods = exposed_rpc_api.requireApi('images/ImagesBrowser');
   
 
  //Test getImagesList
  describe('#getImagesList()', function(){
    it('should ...', function(done){
      //Test the method
      var callback = function(return_value){ 
        //Do your checking here
        done();
      };
      //In case of connection error calls this
      var error_callback = function(data){ 
      };
      //Call the tested method through RPC
      methods.getImagesList( callback, error_callback);
    })
  })

  //Test getSomethingElse
  describe('#getSomethingElse()', function(){
    it('should ...', function(done){
      //Test the method
      var callback = function(return_value){ 
        //Do your checking here
        done();
      };
      //In case of connection error calls this
      var error_callback = function(data){ 
      };
      //Call the tested method through RPC
      methods.getSomethingElse(arg1 ,arg2 ,arg3, callback, error_callback);
    })
  })

  //Test getImage
  describe('#getImage()', function(){
    it('should ...', function(done){
      //Test the method
      var callback = function(return_value){ 
        //Do your checking here
        done();
      };
      //In case of connection error calls this
      var error_callback = function(data){ 
      };
      //Call the tested method through RPC
      methods.getImage(image_id, callback, error_callback);
    })
  })

})
