  //Test ${METHOD_NAME}
  describe('#${METHOD_NAME}()', function(){
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
      methods.${METHOD_NAME}(${ARGS} callback, error_callback);
      //done();
    })
  })