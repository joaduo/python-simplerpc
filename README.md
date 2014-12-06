# python-simplerpc

Python-simplerpc makes it really simple to publish your python webserver API as a client side javacscript API. You can use this library with any existing Python Web framework.

Suppose a class at namespace `myserver.web_api.images.InstantMesseges.InstantMesseges` on javascript can become class at `rpc_api.images.InstantMesseges` with the same methods.

You can point to a python package and python-simplerpc will generate the Javascript API to access the server.

For example, if you have a method `InstantMesseges.send_message(msg)` in python it will become `InstantMesseges.send_message(msg, callback, error_callback)`. As you can see the signature will be the same plus a callback and error_callback functions, since calls to the server are asynchronous.

Other features:

* queuing commands.
* automatic python and javascript unit test mocking. (mocks a unit test per exposed method)
* running tests from controller's module (python's code and javascript code with the help of node.js)
* automatically builds javascript API when python code changes (supported through Web framework autoreload feature)
* you can provide your own templates for javascript API generation

## How does it look like?

If you publish a class that manages an Images Album it would look like:

```python
from simplerpc.expose_api.base.QueueCommandBase import QueueCommandBase

class ImagesBrowser(QueueCommandBase):
    def get_images(self):
    	#return a dictionary with the details of the images
        images = {}
        for img_id in range(20):
            images[img_id] = dict(name='Image%03d' % img_id,
                                  desc='Image %s made by John Doe' % img_id,
                                  url='static/images/Image%03d.jpg' % img_id)
        return images

    def delete_image(self, image_id):
        #here would delete the image
        return True
```

In Javacript the methods above would become:

```javascript
var images = exposed_api.images.ImagesBrowser.get_images(callback, error_callback)
var deleted = exposed_api.images.ImagesBrowser.delete_image(image_id, callback, error_callback)
```

Inheriting from QueueCommandBase means you want to expose all public methods as queue-able methods. (there are more options for API exposition rules: decorating methods, non-queue-able methods for example). Publishing all public, means all methods not starting with a `_` (underscore).

Also, because commands are queued, all of them reach the server through `POST` method. Although this impedes caching you gain some performance having less amount of connections. For using `GET` method, check below.

### A more RESTful like approach

So perhaps you want to have more control over what is published, also you want to control what comes through `GET` and `POST`. Previous example becomes like:

```python
from simplerpc.expose_api.base.ExposedBase import ExposedBase
from simplerpc.expose_api.decorators import expose

class ImagesBrowser(ExposedBase):
    @expose.safe
    def get_images(self):
        images = {}
        return images

    @expose.idempotent
    def delete_image(self, image_id):
        #here would delete the image
        return True
```  

Exposing with `@expose.safe` means it will be served through `GET` method and won't be queued and the request will be inmediate.

To translate to HTTP equivalence

* expose -> POST, Queued
* expose.idempotent -> POST, Queued
* expose.safe -> GET, auto-synched (immediate request)

Right now all methods served through `POST` end up being queued. Later I plan support for auto-synched `POST` methods, they would be published like, E.g.:

```python
    @expose.idempotent.autosync
    def delete_image(self, image_id):
        #here would delete the image
        return True
```

Also `@expose.autosync.idempotent` will be equivalent.

### How to dispatch a request

The `RPCDispatcher` class delivers the message once it is received by the web server. Initialization is:

```python
# Create a context (later i will make contexts non-mandatory)
context = SimpleRpcContext('test_dispatch')

# We need to import the exposed root packages
import myserver.web_api as exposed_api

# Create a dictionary of exposed packages and inner packages
# Inside root's inner packages the dispatcher will be recursive
# We need to specify a root_package were our namespace starts
# in javascript. (this is not optimal, i need to change it) 
dispatcher = RPCDispatcher(context, packages={exposed_api:['images']})
```

Once the dispatcher is initialized you can serve a request like:

```python
from simplerpc.expose_api.decorators import expose

#We need to specify the type of method we want, since have that information from the webserver
result = self.dispatcher.answer(expose.safe, cmd=cmd, args=[], kwargs=kwargs)
```

Where `cmd` is a string like `images.ImagesAlbum.get_images` (cmd for the example above) and `args` and `kwargs` are the arguments passed receiver method.

As you can see you can use this API to connect simplerpc to any Web Framework in python. You need to unpack `cmd`, `args` and  `kwargs` yourself.

For an specific example you can check [Tornado dispatcher file](example_rpc/tornado_handler/JsonRpcHandler.py). That example implements a JsonRPC-like dispatcher over a Tornado framework.

The client side of the RPC protocol can be seen at [RPCCommandsQueue.js](example_rpc/webclient/static/js/simplerpc/rpc/RPCCommandsQueue.js) at the `push` (queuing) and `sync` (sending and receiving) method. 

The protocol format is up to the developer. (you need to specify it on the server and client side)

## Testing a controller's module

Based on the first example the whole module would look like:

```python
from simplerpc.expose_api.base.QueueCommandBase import QueueCommandBase

class ImagesAlbum(QueueCommandBase):
    def get_images(self):
    	#return a dictionary with the details of the images
        images = {}
        for img_id in range(20):
            images[img_id] = dict(name='Image%03d' % img_id,
                                  desc='Image %s made by John Doe' % img_id,
                                  url='static/images/Image%03d.jpg' % img_id)
        return images

    def delete_image(self, image_id):
        #here would delete the image
        return True

#Generate and run tests
if __name__ == "__main__":
    from simplerpc.testing.exposed_api.ExposedModuleAutotester import ExposedModuleAutotester
    auto = ExposedModuleAutotester()
    #Generate tests mock in javascript
    auto.createJsUnitTest(overwrite=False)
    #Run python and javascript tests (in nodejs the later) 
    auto.autoTest()
```

The `ExposedModuleAutotester.createJsUnitTest` will generate a test mock for each method in the controller. The following example is generated based on a jasmine-node template.

```javascript
describe('images/ImagesBrowser', function(){
  //Context and method solver
  var context = require('context').getContext('testing');
  var auto_sync = true;
  var exposed_rpc_api = require('example_rpc/ExposedRpcApi.js')(context, auto_sync);
  var methods = exposed_rpc_api.requireApi('images/ImagesBrowser');
   
 
  //Test get_images
  describe('#get_images()', function(){
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
      methods.get_images( callback, error_callback);
    })
  })

  //same thing for delete_image here ...
  
})
```

Right now the code for generating mocks for python is not there, although the unit test module for this controller can be seen in [ImagesBrowser.py unit test](example_rpc/tests/twin_unittests/exposed_api/images/ImagesBrowser.py).

So when the code reaches `auto.autoTest()` it will run python's and javscript's unit tests and show output results.

## TODO

* document running tests and settings
* get rid of hard-coded parameters in javascript (hostname and port)
* fix class namespace api to expect behavior from `myserver.web_api.images.InstantMesseges.InstantMesseges` becoming `rpc_api.images.InstantMesseges`

Features Whishlist

* enable usage of another javascript compatibility layer (now uses its own one) for using code in Node.js
* extract framework independent javascript code from example_rpc to be used on other frameworks
* make the lib more "protocol agnostic", right now its possible, but not that easy
* check types at client's side (decorating functions at server's side)
* support dispatching to functions (now we only support classes' methods)
* better definition of namespaces in Javascript
* do code style PEP 8 complaint
* receive only the package in Dispatcher omitting subpackages if desired like {exposed_package:exposed_package}
* support exposed package at root level
* integrate a bit more with my [smoothtest](https://github.com/joaduo/smoothtest) framework 

Install and portability

* pypi package
* test on Windows and Mac

## Software requirements

Deploy on Linux OS: (not tested in other platform yet)

* Python 2.7
* Tornado 2.4 (newer probably works)
* Node.js
* jasmine-node
      
## Install and test

1. Install required software:
2. Clone repo `git clone https://github.com/joaduo/python-simplerpc.git`
3. Go to `python-simplerpc`
4. Edit the `simplerpc_settings.py` if you don't have node and `jasmine-node` in your path.
5. Run the unit tests with `python run_tests.py`
6. Start the server with `python webserver.py`
7. Open the web browser in http://localhost:8002  and follow the `API Eplorer` link
