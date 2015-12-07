#!/usr/bin/python
#-*- coding:utf-8 -*-

import httplib,urllib
import socket
import json
import ConfigParser
import sys

def updatedns(params):
    headers = {"User-Agent": "Null's DDNS Updater/0.1.0 (snullp@gmail.com)","Content-type": "application/x-www-form-urlencoded", "Accept": "text/json"}
    conn = httplib.HTTPSConnection("dnsapi.cn")
    conn.request("POST", "/Record.Ddns", urllib.urlencode(params), headers)
    response = conn.getresponse().read()
    conn.close()
    return response

def getip_cn():
    ip = None
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
        ip = None
    return ip

if __name__ == '__main__':
    conf = ConfigParser.RawConfigParser()
    conf.read("domaininfo.ini")
    last_state = ConfigParser.RawConfigParser()
    last_state.read("laststate.ini")

    #change to getip_cn if you are in China mainland
    ip = getip()
    if not ip:
        print "IP fetch failed. You might want to change the ip_fetcher."
        sys.exit(0)

    for site in conf.sections():
        params = {}
        print "Processing "+site+"..."
        if not last_state.has_section(site):
            last_state.add_section(site)

        if last_state.has_option(site, "lastip"):
            last_ip = last_state.get(site, "lastip")
        else:
            last_ip = None

        if ip == last_ip:
            print "IP "+ip+" unchanged"
            continue

        print "IP changed to "+ip
        for param in conf.options(site):
            params[param] = conf.get(site,param)

        data = updatedns(params)

        ret = json.loads(data)
        if ret.get("status",{}).get("code")=="1":
            last_state.set(site,"lastip",ip)
            print "Success."
        else:
            print "Error:", data

    f=open("laststate.ini","w")
    last_state.write(f)
    f.close()
