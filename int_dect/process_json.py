#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import sys
import codecs

from IPython import embed

file_out = 'conn_conf.json'
file_path = 'conns.json'
if len(sys.argv) > 1:
    file_path = sys.argv[1]
    file_out = sys.argv[2]

# JSON List
conn_files = json.load(codecs.open(file_path,'r'))

# Divide into sublist per different port
connections = []
last_port = ''
counter = -1
for item in conn_files:
    # if port is same, append
    if max(item["_source"]["layers"]["tcp.port"]) == last_port:
        connections[counter].append(item)
    # else new conversation
    else:
        last_port = max(item["_source"]["layers"]["tcp.port"])
        counter = counter + 1
        connections.append([item])
with codecs.open(file_out, 'w') as outfile:
    json.dump(connections,outfile)


