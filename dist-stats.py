#!/usr/bin/env python3
import gzip
import sys
import re
import inrdb_bulk

peers = {4: {}, 6: {}}
pfxes = {}

ISO_TIME=sys.argv[2]

with gzip.open(sys.argv[1], 'rt') as inf:
   for line in inf:
      line = line.rstrip('\n')
      fields = line.split()
      peer_ip = fields[0]
      pfx = fields[1]
      plen = fields[2]
      #(peer_ip, pfx, plen) = line.split() # peer pfx len
      af = 4
      if ':' in pfx:
         af = 6
      peers[ af ].setdefault( peer_ip, [] )
      peers[ af ][ peer_ip ].append( int( plen ) )

      pfxes.setdefault( pfx, [] )
      pfxes[ pfx ].append( int( plen ) )

print("# data import finished, starting lookups", file=sys.stderr)

# open persistent connection to INRDB
inrdbSock = inrdb_bulk.MySocket('inrdb-1.ripe.net', 5555)
inrdbline_re=re.compile('(BLOB|RES):\s+(.*)')

def find_country( inrdbSock, pfx, time_iso ):
   #msg = '+dc RIR_STATS %s +xT %s +T +d +M +R\n' % ( pfx, time_iso )
   query = '+dc RIR_STATS %s +xT %s +T +d +M' % ( pfx, time_iso )
   inrdbSock.SendLine(query)
   cc = '--'
   finished=0
   while not finished:
      try:
         answer = inrdbSock.ReceiveLine()
      except IOError:
            break
      if answer[0:5] == 'BLOB:':
         cc = answer.split('|')[1]
      elif answer[0:9] == "Finished:" or answer[0:12] == "Syntax error" or answer[0:22] == "Error paring resource":
            finished = 1
   #print("pfx as: %s %s" % ( pfx, cc ), file=dfd )
   return cc


for (pfx,plens) in pfxes.items():
   #cc = inrdb.find_country( inrdbSock, pfx, ISO_TIME )
   cc = find_country( inrdbSock, pfx, ISO_TIME )
   cnt = len( plens )
   print("PFX", pfx, cnt, min( plens ), max( plens ), cc )

for af in (4,6):
   for (peer,plens) in peers[ af ].items():
      cnt = len( plens )
      print("PEER", af, peer, cnt, min( plens ), max( plens ) )
