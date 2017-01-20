#!/bin/bash

tshark -r  bae7b207833175633c7b61aa99679d2b.pcap -z follow,tcp,ascii,0 -Tjson -e tcp.stream -e  tcp.port -e ip.src -e ip.dst -e tcp.dstport -e ftp.request.command -e ftp.request.arg -e ftp.response.arg -e ftp.response.code -e ftp.response -e ftp.request
