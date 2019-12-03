import urequests, json
from util.octopus import w, web_server
from time import sleep

w()


header = {}
header["Content-Type"] = "application/json"

server = "http://192.168.0.103:5001/api/values"
postdata = '{"name": "abc", "value": 123}'
# postdata = json.loads(postdata)
# print(str(p2))

sleep(3)

for i in range(10):
    print(i)
    postdata = '{"name": "abc", "value":' + str(i) + ' }'
    res = urequests.post(server, data=postdata, headers=header)
    sleep(1)