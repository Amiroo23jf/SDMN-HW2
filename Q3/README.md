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

**Extra**
I have also implemented the code to respond to unexpected POST requests with a 500 status code and the message "Unexpected Request" 
## HTTP_client.py
This script is an example client in order to review the behavior of the server. The client sends the following requests and gets the responses explained in order:
1. GET -> status code 200 with message { "status" : "OK" }
2. POST { "status" : "not OK"} -> status code 201 with message { "status" : "not OK" }
3. GET -> status code 200 with message { "status" : "not OK" }
4. POST { "status" : "OK"} -> status code 201 with message { "status" : "OK" }
5. GET -> status code 200 with message { "status" : "OK" }
