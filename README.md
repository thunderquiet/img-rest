


README


to run: `docker-compose up`

to run tests: 

```
$ cd img-rest
$ python3 -m venv ./venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ pytest test/test.py 
$ cd ../img-engine
$ pip install -r requirements.txt
$ pytest test/test.py 
```

### API endpoints:
We expose three endpoints: 
	POST /resize -> returns a guid id
	GET /resize/<guid> -> returns the processed file
	GET /resize/status/<guid> -> returns the status of the image processing job

The code uses swagger documentation to automatically generate documentation the user can interact with and try the service. It shoould be accessible on the main landing page of the API.



### Architecture:
At the top level, we have two docker containers and a shared mount volume. One container is the API web service running on Python using Flask-restplus framework. The other container is a worker that resizes the images. Communication between them is handled via ZeroMQ messaging tool. The design is flexible enough that it can be extended to handle other types of image transformations in the future with minimal changes.

We decided to save the files to disk in the API service and let the worker pick them up and process them instead of trying to pass raw binary data straight to the worker. This should provide better scalability - the communication between services is now reduced, and memory usage is kept to a minimum. Also this is more stable because if the service goes down most of the unprocessed images are already on disk and we can easily recover. A better design would be to use a database or some other cloud optimized storage such as S3.

We chose to use ZeroMQ for communicating between the two services because it is a light-weight tool and supports various message communication designs. By using something small and simple more server resources can be contributed to the image processing tasks. Communication is currently done via json strings. These are human readable and easy to load/save into a python object. A more efficient approach would have been to send binary data instead. Also, the message format used for communication should be better documented and published. This will enable the development of other APIs that can leverage the same task container.

The project uses a shared configuration file to keep track of paths and hosts between different environments. We tested that everything worked in our local environment (OSX), using docker, as well as while running unit tests.

REST API best practice dictates that our route names should be nouns. However, we used the "resize" verb instead since there is nothing else this API need to do yet. In the future this naming might need to be updated to better reflect the intended business use cases.


We initially considered, but then discarded a few other designs. A publish/subscribe design would not have been appropriate here because we have just 1 instance of the API and worker containers. A webhooks approach would require the worker to make an explicit call back to the API. This would have complicated the design and added extra dependencies. Also, it assume the API is accessible by the workers. This might not be the case if the API is actually running on a local user machine that does not accept inbound connections.



### Future Work:
There are a lot of things we would like to improve with this setup if given the time.

More tests are needed. We need to add tests and update code to handle a number of bad userinput cases. For example, the routes will fail if file is missing or is in wrong format but instead they should return a helpful error message. 

The code uses a number of statements to modify the import path so that modules are all found. That is making it brittle and we should simplify the structure or research some other way to remove those statements.

The worker is currently single-threaded. A better design is to use a thread-pool. This will make it possible to scale up the worker to handle mamy more tasks. 

Finally, the project lacks any integration tests. We need to add tests that verify the communication between containers is happening as expected. 



