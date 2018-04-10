import http.server
import socketserver
import json

PORT = 8006

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
        conn = http.client.HTTPSConnection("api.fda.gov")
        conn.request("GET", "/drug/label.json?limit=10", None, headers)
        r1 = conn.getresponse()
        print(r1.status, r1.reason)
        repos_raw = r1.read().decode("utf-8")
        conn.close()

        d_labelling = json.loads(repos_raw)

        #d_labelling = d_labelling['results']
        #drug_id = "<ol>" + d_labelling[0]['id'] + "<\ol>"

        #message =[]

        #for elem in range(len(d_labelling["results"])):
            #drugs_id = "<ol>" + d_labelling["results"][elem]["id"] + "<\ol>"
            #print(drugs_id)

        # Send message back to client
        message =
            for elem in range(len(d_labelling["results"])):
                drugs_id = "<ol>" + d_labelling["results"][elem]["id"] + "<\ol>"

        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))
        return

Handler = http.server.SimpleHTTPRequestHandler
Handler = testHTTPRequestHandler

httpd = socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT)
httpd.serve_forever()

