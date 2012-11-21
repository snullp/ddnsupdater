#!/usr/bin/python
#-*- coding:utf-8 -*-

import httplib,urllib
import json

def buildquery(email,pwd,did=None):
    params = dict(
        login_email=email,
        login_password=pwd,
        format="json"
    )
    if did!=None: params["domain_id"]=did
    return params

def query(params,api):
    headers = {"User-Agent": "Null's id finder/0.0.1 (snullp@gmail.com)","Content-type": "application/x-www-form-urlencoded", "Accept": "text/json"}
    conn = httplib.HTTPSConnection("dnsapi.cn")
    conn.request("POST", api, urllib.urlencode(params), headers)
    response = conn.getresponse().read()
    conn.close()
    return response

email = raw_input("Your login email please? ")
pwd = raw_input("Password: ")

try:
    params = buildquery(email,pwd)
    ret = json.loads(query(params,"/Domain.List"))
    if ret.get("status",{}).get("code")!="1": raise Exception(ret.get("status",{}).get("message"))
    domains = ret.get("domains",[])
    for domain in domains:
        print domain["name"] + " : " + str(domain["id"])
        params = buildquery(email,pwd,domain["id"])
        ret = json.loads(query(params,"/Record.List"))
        if ret.get("status",{}).get("code")!="1": raise Exception(ret.get("status",{}).get("message"))
        records = ret.get("records",[])
        for record in records:
            #filter A record here
            if record["type"] == "A": print "  " + record["name"] + " : " + str(record["id"])
except Exception as e:
    print "Got exception: " + str(e)
