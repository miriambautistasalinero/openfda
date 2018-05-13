import http.server
import socketserver
import http.client
import json

socketserver.TCPServer.allow_reuse_adress = True

PORT = 8000
class OpenFDAClient():
    #def request_query
    def search_drugs(self, active_ingredient, limit=10):
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

        #search for the active ingredient
        def search_drugs(self, active_ingredient, limit=10)
        elif "searchDrug" in self.path:
            parame =self.path.split("?")[1]
            active_ingredient = parame.split("=")[1].split("&")[0]
            limit = parame.split("&")[1]

            headers = {'User-Agent': 'http-client'}
            query1="/drug/label.json?search=active_ingredient=" + active_ingredient + "&" + limit
            conn = http.client.HTTPSConnection("api.fda.gov")
            conn.request("GET", "/drug/label.json?search=active_ingredient=" + active_ingredient + "&" + limit, None, headers)
            print(query1)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            repos_raw = r1.read().decode("utf-8")
            conn.close()

            d_labelling = json.loads(repos_raw)
            for i in range(len(d_labelling["results"])):
                try:
                    drug_ai = "<li>" + d_labelling["results"][i]["openfda"]["brand_name"][0] + "</li>"
                    self.wfile.write(bytes(str(drug_ai), "utf8"))
                except KeyError:
                    drugai_error = "<li>" + "Not Found" + "</li>"
                    self.wfile.write(bytes(str(drugai_error), "utf8"))


        elif "searchCompany" in self.path:
            parame =self.path.split("?")[1]
            company_name = parame.split("=")[1].split("&")[0]
            limit = parame.split("&")[1]

            headers = {'User-Agent': 'http-client'}
            query = "/drug/label.json?search=openfda.manufacturer_name:" + company_name + "&"+ limit
            conn = http.client.HTTPSConnection("api.fda.gov")
            conn.request("GET", query, None, headers)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            repos_raw = r1.read().decode("utf-8")
            conn.close()

            d_labelling = json.loads(repos_raw)

            for i in range(len(d_labelling["results"])):
                try:
                    drug_mn = "<li>" + d_labelling["results"][i]["openfda"]["brand_name"][0] + "</li>"
                    self.wfile.write(bytes(str(drug_mn), "utf8"))
                except KeyError:
                    companyerror= "<li>" + "Not found" + "</li>"
                    self.wfile.write(bytes(str(companyerror), "utf8"))


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
                try:
                    drug_list = "<li>" + d_labelling["results"][i]["openfda"]["brand_name"][0] + "</li>"
                    self.wfile.write(bytes(str(drug_list), "utf8"))
                except KeyError:
                    drug_error = "<li>" + "Drug Not Found" + "</li>"
                    self.wfile.write(bytes(str(drug_error), "utf8"))


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
                try:
                    company_list = "<li>" + d_labelling["results"][i]["openfda"]["manufacturer_name"][0] + "</li>"
                    self.wfile.write(bytes(str(company_list), "utf8"))

                except KeyError:
                    company_error = "<li>" +"Not Found" + "</li>"
                    self.wfile.write(bytes(str(company_error), "utf8"))

        elif "listWarnings" in self.path:
            parame = self.path.split("?")[1]
            listcompany = parame.split("=")[1]

            headers = {'User-Agent': 'http-client'}

            conn = http.client.HTTPSConnection("api.fda.gov")
            conn.request("GET", "/drug/label.json?limit=" + listcompany, None, headers)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            repos_raw = r1.read().decode("utf-8")
            conn.close()

            d_labelling = json.loads(repos_raw)

            for i in range(len(d_labelling["results"])):
                try:
                    warning = "<li>" + d_labelling["results"][i]["warnings"][0] + "</li>"
                    self.wfile.write(bytes(str(warning), "utf8"))

                except KeyError:
                    warning_error = "<li>" + "Not Found" + "</li>"
                    self.wfile.write(bytes(str(warning_error), "utf8"))



        return

Handler = http.server.SimpleHTTPRequestHandler
Handler = testHTTPRequestHandler

httpd = socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT)
httpd.serve_forever()

