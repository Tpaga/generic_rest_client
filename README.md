# Generic Rest Client

A generic and simple REST client for your python projects.


# How to install

    pip install generic-rest-client

# How to use

## Create your custom class

First you will need to create your own class and extend GenericRestClient, 
for example, lets see our mocky client.

    from api_client import GenericRestClient
    ...
    class MockyRestClient(GenericRestClient):
    ...

## Create custom methods

Every endpoint usually behaves differently, so we will create two functions 
that knows how to handle the requests.

### Obtain all comments

This function knows how to obtain all comments, at least you will have to 
define:

* **Request type**: we know it is a GET request.
* **Endpoint name**: in this case '/comments'
* **Body params**: in this case it is not required
* **Expected http code**: We define HTTP 200 as an expected response.
 
Then we will have: 

    ...
    def get_comments(self):
        ...
        endpoint_url = '/comments'
    
        return self.get_request(
            endpoint_url,
            None,
            [200, ]
        )
    ...
    
### Create a new post

As we said, we create a function that knows what we will need to 
create a new post. To create a new post at least we will have to define: 

* **Request type**: we know it is a POST request.
* **Endpoint name**: in this case '/posts'
* **Body params**: We create a dictionary that contains all the required params.
* **Expected http code**: We define HTTP 201 as an expected response.
 
Then we will have:

	...
	def new_post(self, params):
	    ...
		endpoint_url = '/posts'
		body_params = dict(
			title=params['title'],
			body=params['body'],
		)
		return self.post_request(
			endpoint_url,
			body_params,
			[201, ]
		)
    ...

See? it's really simple. Good luck with your projects! :)

If you want, you can check out our examples section.

# Licence

MIT License

Copyright (c) 2018 Tpaga.co

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

# Our Company

Made with love at [Tpaga](https://tpaga.co), come work with us! jobs@tpaga.co