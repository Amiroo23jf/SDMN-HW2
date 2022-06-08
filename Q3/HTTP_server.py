from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import cgi

PORT = 8000
HOST_NAME = "0.0.0.0"

class PythonServer(BaseHTTPRequestHandler):
    """Python HTTP Server that handles GET and POST request"""
    status = "OK"

    def do_GET(self):
        if self.path == "/api/v1/status":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(json.dumps({"status":self.status}), 'utf-8'))
    
    def do_POST(self):
        if self.path == "/api/v1/status":
            content_length = int(self.headers['Content-Length'])
            try:
                # changes the status and responds to the client
                post_data = self.rfile.read(content_length)
                post_dict = json.loads(post_data.decode('utf-8'))
                PythonServer.status = post_dict["status"]
                self.send_response(201)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(bytes(json.dumps({"status":self.status}), 'utf-8'))
            except:
                # sends unsupported request to the client
                self.send_response(500)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes("Unsupported Request", 'utf-8'))


if __name__=="__main__":
    httpServer = HTTPServer((HOST_NAME, PORT), PythonServer)
    print("Starting server http://localhost:" + str(PORT))

    try:
        print("Server Started.")
        httpServer.serve_forever()
    except KeyboardInterrupt:
        pass
    httpServer.server_close()
    print("Stopping server...")
