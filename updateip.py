#!/usr/bin/python
#-*- coding:utf-8 -*-

import httplib,urllib
import socket
import json

def updatedns(params):
    headers = {"User-Agent": "Null's DDNS Updater/0.0.1 (snullp@gmail.com)","Content-type": "application/x-www-form-urlencoded", "Accept": "text/json"}
    conn = httplib.HTTPSConnection("dnsapi.cn")
    conn.request("POST", "/Record.Ddns", urllib.urlencode(params), headers)
    response = conn.getresponse().read()
    conn.close()
    return response

def getip():
    sock = socket.create_connection(('ns1.dnspod.net', 6666))
    ip = sock.recv(16)
    sock.close()
    return ip

def dictconv(unidict):
    utf8dict=dict()
    for k in unidict:
        if isinstance(unidict[k],basestring):
            utf8dict[k.encode('utf-8')]=unidict[k].encode('utf-8')
        else:
            utf8dict[k.encode('utf-8')]=unidict[k]
    return utf8dict

if __name__ == '__main__':
    f=open('userinfo','r')
    params=dictconv(json.load(f))
    f.close()
    ip = getip()
    try:
        f = open('ipaddr','r+')
    except IOError:
        f = open('ipaddr','w+')
    if ip == f.readline():
        print "IP "+ip+" unchanged"
    else:
        print "IP changed to "+ip+", updating..."
        data = updatedns(params)
        ret = json.loads(data)
        if ret.get("status",{}).get("code")=="1":
            f.truncate(0)
            f.write(ip)
            print "Success."
        else:
            print "Error:"
            print data
    f.close()
