import http.server
import socketserver
import http.client
import json
socketserver.TCPServer.allow_reuse_adress = True

PORT = 8000
# include the logic to communicate with the OpenFDA remote API
class OpenFDAClient():
    def reques_query(self, indi_request,aux,limit):

        headers = {'User-Agent': 'http-client'}
        conn = http.client.HTTPSConnection("api.fda.gov")
        conn.request("GET", "/drug/label.json?search=" + indi_request + aux +"&limit" + limit, None, headers)
        r1 = conn.getresponse()
        print(r1.status, r1.reason)
        repos_raw = r1.read().decode("utf-8")
        conn.close()

        d_labelling = json.loads(repos_raw)
        return d_labelling

    #def search_drugs(self, active_ingredient, limit=10):
        #indi_req = "/drug/label.json?search=active_ingredient=" + active_ingredient + "&" + limit
        #text = self.send_query(indi_req)

        #return text

    #def search_company(self,company_name, limit=10):
        #indi_req = "/drug/label.json?search=openfda.manufacturer_name:" + company_name + "&"+ limit
        #text = self.send(indi_req)
        #return text

    #def list_drugs(self, limit=10):
        #indi_req="/drug/label.json?limit=" + limit
        #text =self.send(indi_req)
        #return text

#includes the logic to extract the data from drugsitems
class OpendFDAParser():

    def parse_drugs(self, d_labelling):

        stuff=[]
        for i in range(len(d_labelling["results"])):
            if 'openfda' in "results" and 'active_ingredient' in d_labelling["results"]['openfda']:
                stuff.append(d_labelling["results"][i]["openfda"]["brand_name"][0])
            else:
                stuff.append("Not Found")
        return stuff

    def parse_compnies(self, d_labelling):

        stuff=[]

        for i in range(len(d_labelling["results"])):
            if 'openfda' in "results" and 'manufacturer_name' in d_labelling["results"]['openfda']:
                stuff.append(d_labelling["results"][i]["openfda"]["brand_name"][0])
            else:
                stuff.append("Not Found")
        return stuff

    def parse_warnings(self, d_labelling):

        stuff=[]
        for i in range(len(d_labelling["results"])):
            if 'openfda' in "results" and 'warnings' in d_labelling["results"]['openfda']:
                stuff.append(d_labelling["results"][i]["warnings"][0])
            else:
                stuff.append("Not Found")
        return stuff

class OpenFDAhtml():

    def new_html(self, stuff):

        n_html = "<ul>"

        for elem in stuff:
            n_html += "<li>" + elem + "</li>"
        n_html += "</ul>"

        return n_html

    #def send_file(self, file):
        #with open(file, "r") as f:
            #content = f.read()
        #print(file, "is to be sent")
        #return content

class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    # GET
    def do_GET(self):

        client =OpenFDAClient()
        searcher = OpendFDAParser()
        html= OpenFDAhtml()

        limit_dfv = "10"
        message =""
        infor=""
        aux=""
        code=200

        if self.path == "/":
            with open("search.html", "r") as s: #we open search
                message = s.read()#lee search y lo ejecuta

        elif "searchDrug" in self.path:
            parame =self.path.split("?")[1]
            aux = parame.split("=")[1].split("&")[0]
            if parame.split("&")[1] =="":
                limit = limit_dfv
            else:
                limit= parame.split("&")[1]

            indi_req = "active_ingredient="
            sure = client.reques_query(indi_req,aux,limit)
            infor = searcher.parse_drugs(sure)
            message = html.new_html(infor)

        elif "searchCompany" in self.path:
            parame =self.path.split("?")[1]
            company_name = parame.split("=")[1].split("&")[0]
            if parame.split("&")[1] == '':
                limit = str(10)
            else:
                limit = parame.split("&")[1]
            indi_req = "/drug/label.json?search=openfda.manufacturer_name:" + company_name + "&" + limit
            drugs = client.reques_query(self, indi_req, limit_dfv)
            infor = searcher.parse_drugs(drugs)
            message = html.new_html(infor)

        elif "listDrug" in self.path:
            parame = self.path.split("?")[1]
            if parame.split("=")[1] == '':
                listdrug = limit_dfv
            else:
                listdrug = parame.split("=")[1]
            indi_req = "/drug/label.json?limit=" + listdrug
            drugs = client.reques_query(self, indi_req, limit_dfv)
            infor = searcher.parse_drugs(drugs)
            message = html.new_html(infor)


        elif "listCompany" in self.path:
            parame = self.path.split("?")[1]
            if  parame.split("=")[1]=="":
                listcompany = limit_dfv
            else:
                listcompany = parame.split("=")[1]
            indi_req = "/drug/label.json?limit=" + listcompany
            drugs = client.reques_query(self, indi_req, limit_dfv)
            infor = searcher.parse_drugs(drugs)
            message = html.new_html(infor)

        elif "listWarnings" in self.path:
            parame = self.path.split("?")[1]
            if parame.split("=")[1] == "":
                listwarnings = limit_dfv
            else:
                listwarnings = parame.split("=")[1]
            indi_req = "/drug/label.json?limit=" + listwarnings
            drugs = client.reques_query(self, indi_req, limit_dfv)
            infor = searcher.parse_drugs(drugs)
            message = html.new_html(infor)

        elif 'secret' in self.path:
            code = 401

        elif 'redirect' in self.path:
            code = 302

        else:
            code = 404
            with open('error.html', 'r') as f:
                http_res = f.read()

        # Send response status code
        self.send_response(code)

        # Send the correct header
        if 'secret' in self.path:
            self.send_header('WWW-Authenticate', 'Basic realm="OpenFDA Private Zone"')
            self.end_headers()
        elif 'redirect' in self.path:
            self.send_header('Location', 'http://localhost:8000/')
            self.end_headers()
        else:
            self.send_header('Content-type', 'text/html')
            self.end_headers()

        self.wfile.write(bytes(str(message), "utf8"))
        return

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











