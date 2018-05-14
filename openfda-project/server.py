import http.server
import socketserver
import http.client
import json

socketserver.TCPServer.allow_reuse_address = True

# -- IP and the port of the server
IP = "localhost"  # Localhost means "I": your local machine
PORT = 8000


class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        status = 200
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Send message back to client

        def send_file(file):
            with open(file) as f:
                message = f.read()
            self.wfile.write(bytes(message, "utf8"))

        def search_ingredient(active_ingredient, limit):


            headers = {'User-Agent': 'http-client'}

            conn = http.client.HTTPSConnection("api.fda.gov")
            conn.request("GET", "/drug/label.json?search=active_ingredient:%s&limit=%s" % (active_ingredient, limit),
                         None, headers)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            repos_raw = r1.read().decode("utf-8")
            conn.close()

            d_labelling = json.loads(repos_raw)

            with open("info.html", "w"):
                self.wfile.write(bytes("<ol>" + "\n", "utf8"))
                for i in range(len(d_labelling["results"])):
                    try:
                        drug_ai = "<li>" + d_labelling["results"][i]["openfda"]["brand_name"][0] + "</li>"
                        self.wfile.write(bytes(str(drug_ai), "utf8"))
                    except KeyError:
                        drugai_error = "<li>" + "Not Found" + "</li>"
                        self.wfile.write(bytes(str(drugai_error), "utf8"))

        def search_company(company, limit):

            print(str(self.path))

            headers = {'User-Agent': 'http-client'}

            conn = http.client.HTTPSConnection("api.fda.gov")
            conn.request("GET", "/drug/label.json?search=openfda.manufacturer_name:%s&limit=%s" % (company, limit),
                         None, headers)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            repos_raw = r1.read().decode("utf-8")
            conn.close()

            d_labelling = json.loads(repos_raw)

            with open("info.html", "w"):
                self.wfile.write(bytes("<ol>" + "\n", "utf8"))
                for i in range(len(d_labelling["results"])):
                    try:
                        drug_mn = "<li>" + d_labelling["results"][i]["openfda"]["brand_name"][0] + "</li>"
                        self.wfile.write(bytes(str(drug_mn), "utf8"))
                    except KeyError:
                        companyerror = "<li>" + "Not found" + "</li>"
                        self.wfile.write(bytes(str(companyerror), "utf8"))

        def list_drugs(limit):

            print(str(self.path))

            headers = {'User-Agent': 'http-client'}

            conn = http.client.HTTPSConnection("api.fda.gov")
            conn.request("GET", "/drug/label.json?limit=%s" % (limit), None, headers)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            repos_raw = r1.read().decode("utf-8")
            conn.close()

            d_labelling = json.loads(repos_raw)

            with open("info.html", "w"):
                self.wfile.write(bytes("<ol>" + "\n", "utf8"))
                for i in range(len(d_labelling["results"])):
                    try:
                        drug_list = "<li>" + d_labelling["results"][i]["openfda"]["brand_name"][0] + "</li>"
                        self.wfile.write(bytes(str(drug_list), "utf8"))
                    except KeyError:
                        drug_error = "<li>" + "Drug Not Found" + "</li>"
                        self.wfile.write(bytes(str(drug_error), "utf8"))

        def list_companies(limit):

            print(str(self.path))

            headers = {'User-Agent': 'http-client'}

            conn = http.client.HTTPSConnection("api.fda.gov")
            conn.request("GET", "/drug/label.json?limit=%s" % (limit), None, headers)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            repos_raw = r1.read().decode("utf-8")
            conn.close()

            d_labelling = json.loads(repos_raw)

            with open("info.html", "w"):
                self.wfile.write(bytes("<ol>" + "\n", "utf8"))
                for i in range(len(d_labelling["results"])):
                    try:
                        company_list = "<li>" + d_labelling["results"][i]["openfda"]["manufacturer_name"][0] + "</li>"
                        self.wfile.write(bytes(str(company_list), "utf8"))

                    except KeyError:
                        company_error = "<li>" + "Not Found" + "</li>"
                        self.wfile.write(bytes(str(company_error), "utf8"))

        def list_warnings(limit):

            print(str(self.path))

            headers = {'User-Agent': 'http-client'}

            conn = http.client.HTTPSConnection("api.fda.gov")
            conn.request("GET", "/drug/label.json?limit=%s" % (limit), None, headers)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            repos_raw = r1.read().decode("utf-8")
            conn.close()

            d_labelling = json.loads(repos_raw)

            with open("info.html", "w"):
                self.wfile.write(bytes("<ol>" + "\n", "utf8"))
                for i in range(len(d_labelling["results"])):
                    try:
                        warning = "<li>" + d_labelling["results"][i]["warnings"][0] + "</li>"
                        self.wfile.write(bytes(str(warning), "utf8"))

                    except KeyError:
                        warning_error = "<li>" + "Not Found" + "</li>"
                        self.wfile.write(bytes(str(warning_error), "utf8"))

        path = self.path

        if path == "/":
            with open("search.html") as f:
                message = f.read()
            self.wfile.write(bytes(message, "utf8"))

        elif 'searchDrug' in path:
            active_ingredient = path.split("=")[1].split("&")[0]
            if "limit" in path:
                limit = path.split("=")[2]
                if limit == '':
                    limit = 10
            else:
                limit = '10'
            search_ingredient(active_ingredient, limit)
            file = 'info.html'
            send_file(file)

        elif 'searchCompany' in path:
            company = path.split("=")[1].split("&")[0]
            if "limit" in path:
                limit = path.split("=")[2]
                if limit == '':
                    limit = 10
            else:
                limit = '10'
            search_company(company, limit)
            file = 'info.html'
            send_file(file)

        elif 'listDrugs' in path:
            if 'limit' in path:
                limit = path.split("=")[1].split("&")[0]
                if limit == '':
                    limit = 10
            else:
                limit = '10'
            list_drugs(limit)
            file = 'info.html'
            send_file(file)

        elif 'listCompanies' in path:
            if 'limit' in path:
                limit = path.split("=")[1].split("&")[0]
                if limit == '':
                    limit = 10
            else:
                limit = '10'
            list_companies(limit)
            file = 'info.html'
            send_file(file)

        elif 'listWarnings' in path:
            if 'limit' in path:
                limit = path.split("=")[1].split("&")[0]
                if limit == '':
                    limit = 10
            else:
                limit = '10'
            list_warnings(limit)
            file = 'info.html'
            send_file(file)
        elif "secret" in path:
            status +=401
            print("You are nor authorized!Code:"+ status)

        elif "redirect" in path:
            status += 302
            print("You are being redirected. Code:" + status)
        else:
            status +=404
            with open("not_found.html") as f:
                message = f.read()
            self.wfile.write(bytes(message, "utf8"))

        self.send_response(status)

        if "secret" in path:
            self.send_header('WWW-Authenticate', 'Basic realm="OpenFDA Private Zone"')
            self.end_headers()
        elif "redirect" in path:
            self.send_header('Location', 'http://localhost:8000/')
            self.end_headers()
        else:
            self.send_header('Content-type', 'text/html')
            self.end_headers()
        #self.send_header('Content-type', 'text/html')
        #self.end_headers()


        print("Done")

        return


# Handler = http.server.SimpleHTTPRequestHandler
Handler = testHTTPRequestHandler

httpd = socketserver.TCPServer((IP, PORT), Handler)
print("serving at port", PORT)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    pass

httpd.server_close()
print("")
print("Server stopped!")
