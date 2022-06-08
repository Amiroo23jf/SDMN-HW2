In this Question, an HTTP server is created which responds to GET and POST requests in the way explained.

## HTTP_server.py
This script creates an HTTP server which responds to GET requests with status code 200 and a json file with the format below:
```
{ "status" : "<Current Status>"}
```
where the parameter <Current Status> can be changed using POST requests.

In order to change the status, a POST request with the given format should be sent to the server:
```
{ "status" : "<Current Status>"}
```
By sending this request to the server, the servers responds with status code 201 and changes the <Current Status> to the given value.
