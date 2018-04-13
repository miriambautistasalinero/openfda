import http.server
import socketserver
import json
import http.client

# -- IP and the port of the server
IP = "localhost"  # Localhost means "I": your local machine
PORT = 8002


# HTTPRequestHandler class
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    # GET
    def do_GET(self):
        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        headers = {'User-Agent': 'http-client'}

        conn = http.client.HTTPSConnection("api.openfda.gov")
        conn.request("GET", "/drug/label.json?limit=10", None, headers)
        r1 = conn.getresponse()
        print(r1.status, r1.reason)
        repos_raw = r1.read().decode("utf-8")
        conn.close()
        print("hola")

        d_labelling = json.loads(repos_raw)

        # Send message back to clien

        for elem in range(len(d_labelling["results"])):
            drugs_id = "<ol>" + d_labelling["resulst"][elem]["id"] + "<\ol>"
            print(drugs_id)



# Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))
        print("File served!")
        return


# Handler = http.server.SimpleHTTPRequestHandler
Handler = testHTTPRequestHandler

httpd = socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    pass

httpd.server_close()
print("")
print("Server stopped!")


# https://github.com/joshmaker/simple-python-webserver/blob/master/server.py
