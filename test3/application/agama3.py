# import subprocess
import datetime, platform, httpx, json
from flask import request
# from .agama3db import db_log_add

octopusASCII = [
"      ,'''`.",
"     /      \ ",
"     |(@)(@)|",
"     )      (",
"    /,'))((`.\ ",
"   (( ((  )) ))",
"   ) \ `)(' / ( ",
]


def print_octopus(spaces=2):
    rs = "\n"
    for ol in octopusASCII:
        rs += " "*spaces + str(ol) + "\n"
    rs += "\n"
    return rs


def remote_addr():
   try:
      rs = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
   except:
      rs = "???"
   return rs


def system_info():
    rs =""
    #rs += "procesor: " + platform.processor() + "\n"
    rs += "platform: " + platform.platform() + " | \n"
    rs += "version: " + platform.version() + " | \n"
    rs += remote_addr() + "\n   "
    rs +=  "\n"
    return rs

def bitcoin_usd():
   res = httpx.get("https://api.coinpaprika.com/v1/tickers/btc-bitcoin")
   btcusd = res.json()['quotes']["USD"]["price"]
   return int(float(btcusd))
