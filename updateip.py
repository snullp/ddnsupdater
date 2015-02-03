#!/usr/bin/python
#-*- coding:utf-8 -*-

import httplib,urllib
import socket
import json
import ConfigParser

def updatedns(params):
    headers = {"User-Agent": "Null's DDNS Updater/0.1.0 (snullp@gmail.com)","Content-type": "application/x-www-form-urlencoded", "Accept": "text/json"}
    conn = httplib.HTTPSConnection("dnsapi.cn")
    conn.request("POST", "/Record.Ddns", urllib.urlencode(params), headers)
    response = conn.getresponse().read()
    conn.close()
    return response

def getip_cn():
    ip = '0.0.0.0'
    try:
        sock = socket.create_connection(('ns1.dnspod.net', 6666))
        ip = sock.recv(16)
        sock.close()
    except socket.error:
        pass
    return ip

def getip():
    ip = urllib.urlopen('http://ip.appspot.com').read().strip()
    try:
        socket.inet_aton(ip)
    except socket.error:
        ip = '0.0.0.0'
    return ip

if __name__ == '__main__':
    conf = ConfigParser.RawConfigParser()
    conf.read("domaininfo.ini")

#change to getip_cn if you are in China mainland
    ip = getip()

    for site in conf.sections():
        params = {}
        print "Processing "+site+"..."
        try:
            for param in conf.options(site):
                if param == "lastip":
                    if ip == conf.get(site,param):
                        raise Warning
                else: params[param] = conf.get(site,param)
            print "IP changed to "+ip
            data = updatedns(params)
            ret = json.loads(data)
            if ret.get("status",{}).get("code")=="1":
                conf.set(site,"lastip",ip)
                print "Success."
            else:
                print "Error:"
                print data
        except Warning:
            print "IP "+ip+" unchanged"

    f=open("domaininfo.ini","w")
    conf.write(f)
    f.close()
