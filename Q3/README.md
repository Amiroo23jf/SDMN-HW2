In this Question, an HTTP server is created which responds to GET and POST requests in the way explained.

## HTTP_server.py
This script creates an HTTP server which responds to GET requests with status code 200 and a json file with the format below:
```
{ "status" : "<Current Status>"}
```
where the parameter `Current Status` can be changed using POST requests.

In order to change the status, a POST request with the given format should be sent to the server:
```
{ "status" : "<Current Status>"}
```
By sending this request to the server, the servers responds with status code 201 and changes the `Current Status` to the given value.

**Extra:**
I have implemented the functionality that the server responds to unexpected POST requests with status code 500 and and html message "Unsupported Requested"

## HTTP_client.py
The script acts as an example client that send the requests given below in order and prints their response in order to check the functionality of the server:
1. GET -> status code 200, message { "status" : "OK" }
2. POST { "status" : "not OK" } -> status code 201, message { "status" : "not OK" }
3. GET -> status code 200, message { "status" : "OK" }
4. POST { "status" : "not OK" } -> status code 201, message { "status" : "OK" }
5. GET -> status code 200, message { "status" : "not OK" }
