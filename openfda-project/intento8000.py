import http.server
import socketserver
import http.client
import json
socketserver.TCPServer.allow_reuse_adress = True

PORT = 8000
# include the logic to communicate with the OpenFDA remote API
class OpenFDAClient():
    def reques_query(self, indi_req):

        where = "/drug/label.json"
        final_request= where + '?' + indi_req
        headers = {'User-Agent': 'http-client'}
        conn = http.client.HTTPSConnection("api.fda.gov")
        conn.request("GET", final_request, None, headers)
        r1 = conn.getresponse()
        print(r1.status, r1.reason)
        repos_raw = r1.read().decode("utf-8")
        conn.close()

        d_labelling = json.loads(repos_raw)
        return d_labelling

    def search_drugs(self, active_ingredient, limit=10):
        parame = self.path.split("?")[1]
        active_ingredient = parame.split("=")[1].split("&")[0]
        limit = parame.split("&")[1]
        indi_req = "/drug/label.json?search=active_ingredient=" + active_ingredient + "&" + limit
        text = self.send_query(indi_req)

        return text

    def search_company(self,company_name, limit=10):
        parame = self.path.split("?")[1]
        company_name = parame.split("=")[1].split("&")[0]
        limit = parame.split("&")[1]

        indi_req = "/drug/label.json?search=openfda.manufacturer_name:" + company_name + "&"+ limit
        text = self.send(indi_req)
        return text

    def list_drugs(self, limit=10):
        parame = self.path.split("?")[1]
        listdrug = parame.split("=")[1]

        indi_req="/drug/label.json?limit=" + listdrug
        text =self.send(indi_req)
        return text

#includes the logic to extract the data from drugsitems
class OpendFDAParser():

    def parse_drugs(self, d_labelling):


