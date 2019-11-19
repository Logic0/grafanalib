#!/usr/local/bin/python3
#-*-coding:utf-8

'''
HOST http://1.1.8.1/
POST /api/dashboards/db HTTP/1.1
Accept: application/json
Content-Type: application/json
Authorization: Bearer eyJrIjoaTRObWJldWE1cG5vRzQiLCJuIjoiYXV0by1kYXNoYm9hcmQiLCJpZCI6MX0=

{
  "dashboard": {
    "id": null,
    "uid": null,
    "title": "Production Overview",
    "tags": [ "templated" ],
    "timezone": "browser",
    "schemaVersion": 16,
    "version": 0
  },
  "folderId": 0,
  "overwrite": false
}
'''

import sys
import requests
import json

# Grafana 创建视图的 API restful 地址
URL = "http://IP:Port/api/dashboards/db"
HEADERS = { "Accept": "application/json", 
            "Content-Type": "application/json", 
            "Authorization":"Bearer + 空格 + 在 Grafana 上申请的 api key"}

# create API request body
body = {"folderid": 0, "overwrite": True }

if len( sys.argv ) < 2:
    print( "Usage: %s dashboard.json" % sys.argv[0] )
else:
    boardcontent = open( sys.argv[1] ).read()
    jsonobj = json.loads( boardcontent )
    body["dashboard"] = jsonobj
    #print( HEADERS )
    #print( body )
    rsp = requests.post( URL, headers = HEADERS, data = json.dumps( body )  )

    print( rsp.text )
