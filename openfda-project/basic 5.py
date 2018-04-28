import http.server
import socketserver
import http.client
import json

socketserver.TCPServer.allow_reuse_adress = True

PORT = 8000

# HTTPRequestHandler class
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    # GET
    def do_GET(self):

       # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type','text/html')
        self.end_headers()

        # Send message back to client
        message = ''
        if self.path == "/":
            with open("basicfinal.html", "r") as s: #we open search
                message = s.read()#lee search y lo ejecuta
            self.wfile.write(bytes(message, "utf8")) #esto es lo que le llega al cliente
        #en caso de que tenga más parametros que solo \
        elif "search?" in self.path:
            parame = self.path.split("?")[1]
            drug = parame.split("&")[0].split("=")[1]
            limit = parame.split("&")[1].split("=")[1]

            headers = {'User-Agent': 'http-client'}

            conn = http.client.HTTPSConnection("api.fda.gov")
            conn.request("GET", "/drug/label.json?search=generic_name:" + drug + "&limit=" + limit , None, headers)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            repos_raw = r1.read().decode("utf-8")
            conn.close()

            d_labelling = json.loads(repos_raw)
            self.wfile.write(bytes(str(d_labelling), "utf8"))

        #search for the active ingredient
        elif "searchDrug" in self.path:
            parame =self.path.split("?")[1]
            active_ingredient = parame.split("=")[1]
            limit = parame.split("&")[1].split("=")[1]

            headers = {'User-Agent': 'http-client'}

            conn = http.client.HTTPSConnection("api.fda.gov")
            conn.request("GET", "/drug/label.json?search=active_ingredient=" + active_ingredient + "&limit=" + limit, None, headers)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            repos_raw = r1.read().decode("utf-8")
            conn.close()

            d_labelling = json.loads(repos_raw)

            for elem in range(len(d_labelling["results"])):
                drug_ai = "<li>" + d_labelling["results"][elem]["openfda"]["brand_name"][0] + "</li>"

                self.wfile.write(bytes(str(drug_ai), "utf8"))

        elif "searchCompany" in self.path:
            parame =self.path.split("?")[1]
            company_name = parame.split("=")[1]
            limit = parame.split("&")[1].split("=")[1]

            headers = {'User-Agent': 'http-client'}

            conn = http.client.HTTPSConnection("api.fda.gov")
            conn.request("GET", "/drug/label.json?search=openfda.manufacturer_name:" + company_name + "&limit=" + limit, None, headers)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            repos_raw = r1.read().decode("utf-8")
            conn.close()

            d_labelling = json.loads(repos_raw)

            for elem in range(len(d_labelling['results'])):
                drug_mn = "<li>" + d_labelling["results"][elem]["openfda"]["brand_name"][0] + "</li>"

                self.wfile.write(bytes(str(drug_mn), "utf8"))

        elif "listDrug" in self.path:
            parame = self.path.split("?")[1]
            listdrug = parame.split("=")[1]

            headers = {'User-Agent': 'http-client'}

            conn = http.client.HTTPSConnection("api.fda.gov")
            conn.request("GET", "/drug/label.json?limit=" + listdrug , None, headers)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            repos_raw = r1.read().decode("utf-8")
            conn.close()

            d_labelling = json.loads(repos_raw)

            for i in range(len(d_labelling["results"])):
                drug_list = "<li>" + d_labelling["results"][i]["openfda"]["brand_name"][0] + "</li>"

                self.wfile.write(bytes(str(drug_list), "utf8"))

        elif "listCompany" in self.path:
            parame = self.path.split("?")[1]
            listcompany = parame.split("=")[1]

            headers = {'User-Agent': 'http-client'}

            conn = http.client.HTTPSConnection("api.fda.gov")
            conn.request("GET", "/drug/label.json?limit=" + listcompany , None, headers)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            repos_raw = r1.read().decode("utf-8")
            conn.close()

            d_labelling = json.loads(repos_raw)

            for i in range(len(d_labelling["results"])):
                company_list = "<li>" + d_labelling["results"][i]["openfda"]["manufacturer_name"][0] + "</li>"

                self.wfile.write(bytes(str(company_list), "utf8"))

        return

    #search este dentro de self.path

Handler = http.server.SimpleHTTPRequestHandler
Handler = testHTTPRequestHandler

httpd = socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT)
httpd.serve_forever()

