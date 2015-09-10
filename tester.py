#!/usr/bin/python3

import requests
import time
from requests.adapters import HTTPAdapter

proxyfile = "proxy.txt"
logfile = "log.txt"
url = "http://monip.org"

def log(string):
    with open(logfile, "a+") as f:
        f.write(string)

def getlog():
    try:
        with open(logfile, "r") as f:
            return f.read()
    except IOError as e:
        return ""

def test_proxy(proxy):
    proxy = proxy.replace("\n", "").split(" ")[0]
    if len(proxy) < 4:
        return
    if proxy in getlog():
        print("Proxy already tested")
        return
    http_proxy  = "http://%s" %proxy
    https_proxy = "https://%s" %proxy
    ftp_proxy   = "ftp://%s" %proxy
    proxyDict = { 
              "http"  : http_proxy,
              "https" : https_proxy, 
              "ftp"   : ftp_proxy
            }
    try:
        print("Testing proxy %s" %proxy)
        s = requests.Session()
        #s.mount(url, HTTPAdapter(max_retries=5))
        start = time.time()
        r = s.get(url, proxies=proxyDict)
        end = time.time()
        print("Proxy seems UP !\nAnswered in : %s" %(end-start))
        if "detected" in r.text:
            print("Proxy detected by monip.org")
            log("%s;%s;%s\n" %(proxy, "1", end-start))
        else:
            log("%s;%s;%s\n" %(proxy, "0", end-start))
    except Exception as e:
        print("Proxy seems down")
        log("%s;%s;%s\n" %(proxy, "0", "-1"))
        print(e)

def main():
    proxies = []
    with open(proxyfile, "r") as f:
        proxies = f.readlines()
    for proxy in proxies:
        test_proxy(proxy)
    return 0

if __name__ == "__main__":
    main()
