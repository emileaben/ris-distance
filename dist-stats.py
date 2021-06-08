#!/usr/bin/env python3
import gzip
import sys
import inrdb

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


for (pfx,plens) in pfxes.items():
   cc = inrdb.find_country( pfx, ISO_TIME )
   cnt = len( plens )
   print("PFX", pfx, cnt, min( plens ), max( plens ), cc )

for af in (4,6):
   for (peer,plens) in peers[ af ].items():
      cnt = len( plens )
      print("PEER", af, peer, cnt, min( plens ), max( plens ) )
