#!/usr/bin/env python3
import os
import sys
import json
from urllib.request import urlopen, Request
import urllib.error
from datetime import datetime
from datetime import timezone
import datetime
import asyncio
import time
import requests
from dapnet_api import DAPNET

url = "https://hams.at/api/alerts/upcoming"
hamsat_api_key = '<HAMSAT_API_KEY>'

dapnet_user = '<DAPNET_USER>'
dapnet_pass = '<DAPNET_PASS>'
dapnet_recipient = ['<DAPNET_RECIPIENTS>']
dapnet_groups = ['<DAPNET_GROUPS>']

def dapnet_msg(msg):
    client = DAPNET(dapnet_user, dapnet_pass)
    client.send_message(msg, dapnet_recipient, dapnet_groups)

try:
    page = urlopen(Request(url, headers={'User-Agent': 'Mozilla', 'Authorization': 'Bearer '+hamsat_api_key}))
except urllib.error.HTTPError as e:
    print("Error fetching hams.at page")
    os.remove(destination)
    sys.exit()
except urllib.error.URLError as e:
    print("Error fetching hams.at page")
    os.remove(destination)
    sys.exit()
else:
    data = json.load(page)
    activations = []
    new_activations = []
    source='hamsat.txt'
    if not os.path.exists(source):
        f = open(source, "x")
    with open(source, 'r') as fin:
        activations = fin.read().splitlines()
    acts = []
    for act in data['data']:
        dt = datetime.datetime.now(timezone.utc)
        utc_time = dt.replace(tzinfo=timezone.utc)
        utc_timestamp = utc_time.timestamp()
        ts_aos = datetime.datetime.strptime(act['aos_at'], '%Y-%m-%dT%H:%M:%SZ')
        ts_aos_utc = ts_aos.replace(tzinfo=timezone.utc)
        ts_workable_start = 0;
        ts_workable_start_utc = 0;
        if (act['workable_start_at']):
            ts_workable_start = datetime.datetime.strptime(act['workable_start_at'], '%Y-%m-%dT%H:%M:%SZ')
            ts_workable_start_utc = ts_workable_start.replace(tzinfo=timezone.utc)
        grids =[] 
        gridlist = ' / '.join(grids)
        acts.append(act['id'])
        if act['id'] not in activations:
            if act['is_workable']:
                ts_los = datetime.datetime.strptime(act['los_at'], '%Y-%m-%dT%H:%M:%SZ')
                ts_los_utc = ts_los.replace(tzinfo=timezone.utc)
                ts_workable_end = datetime.datetime.strptime(act['workable_end_at'], '%Y-%m-%dT%H:%M:%SZ')
                ts_workable_end_utc = ts_workable_end.replace(tzinfo=timezone.utc)

                pager_msg = act['callsign']+" on "+act['satellite']['name']+" from "+gridlist+" at "
                if ts_workable_start_utc.strftime("%Y-%m-%d") != utc_time.strftime('%Y-%m-%d'):
                    pager_msg = pager_msg+ts_workable_start_utc.strftime("%Y-%m-%d")+" "
                pager_msg = pager_msg+ts_workable_start_utc.strftime("%H%Mz")
                if act['comment']:
                    pager_msg = pager_msg+": "+act['comment']
                dapnet_msg(pager_msg)
        new_activations.append(act['id'])
    for act in activations:
        if act not in acts and act in new_activations:
            new_activations.remove(act)
    destination='hamsat_new.txt'
    fout = open(destination, "w")
    for act in new_activations:
        fout.write(act+"\n")
    fin.close()
    fout.close()
    os.rename(destination,source)
sys.exit()
