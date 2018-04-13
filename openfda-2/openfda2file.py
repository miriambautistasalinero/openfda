import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json?search=active_ingredient:\"acetylsalicylic\"&limit=4", None, headers)
#Wehn we search for acetylsalicylic the total number is 4
r1 = conn.getresponse()
print(r1.status, r1.reason)
repos_raw = r1.read().decode("utf-8")
conn.close()

repos = json.loads(repos_raw)

#print("The id of the first drug is", repos["results"][0]["id"])
#print("The purpose is", repos["results"][0]["purpose"])
#print("The manufacter is", repos["results"][0]["openfda"]["manufacturer_name"])

for elem in range(len(repos["results"])):
    try:
        print("The manufacter is", repos["results"][elem]["openfda"]["manufacturer_name"])
    except KeyError:
        continue