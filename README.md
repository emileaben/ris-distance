# ris-distance
how far is the Internet from the RIS route collector

# scripts description
   * doit.sh : main file that drives the analysis
(note that parts of this can only be run from NCC network, as it needs access to an internal database (sg-inrdb) for prefix->country lookups. could be replaced by something that downloads rir-stats.

# data files generated
## peer.pfx.pathlen.$YYYY.$MM.$DD.txt.gz
Contains stats on how far peers are from prefixes. fields:
   * ris peer ip
   * prefix
   * as pathlength (inflation (inpending/prepending/path poisoning) removed)
   * original as pathlength
   * has_duplicate ASNs (ie. previous 2 fields are different) , (0,1)
   * has path_poisoning , (0,1)
   
example:
```
102.67.56.1 1.0.0.0/24 2 2 0 0
103.102.5.1 1.0.0.0/24 2 2 0 0
103.212.68.10 1.0.0.0/24 2 2 0 0
```

## stats.$YYYY.$MM.$DD.txt.gz :
Contains overall stats for a prefix (first field: PFX) or a peer (first field: PEER).
For PFX:
   * literal: PFX
   * prefix
   * 'power' (ie. how many RIS peers saw this prefix)
   * min pathlength ( inflation removed )
   * max pathlength ( inflation removed )
   * country code (per RIR-stats), '--' if we didn't resolve via RIR stats
   
example:
```
PFX 1.0.0.0/24 383 2 4 AU
PFX 1.0.4.0/22 396 3 6 AU
PFX 1.0.4.0/24 397 2 6 AU
PFX 1.0.5.0/24 397 2 5 AU
```

For PEER:
   * literal: PEER
   * address family (a single peer can see both v4 and v6 prefixes, in that case it is listed twice in this file, once for v4, once for v6)
   * peer IP
   * number of prefixes seen for this address family
   * min pathlength seen ( inflation removed )
   * max pathlength seen ( inflation removed )
   
example:
```
PEER 4 102.67.56.1 838776 1 13
PEER 4 103.102.5.1 856237 1 13
PEER 4 103.212.68.10 875841 1 12
PEER 4 109.248.43.5 5617 2 6
PEER 4 12.0.1.63 830953 1 11
```

## improvements.$YYYY.$MM.$DD.txt :
Contains suggestions for improvements, based on the topology we observe in RIS. This doesn't take into account that there is likely hidden topology (AS links for p2p peers) that we can't predict from the data
fields:
    * geo area: "GLOBAL" or a ISO 2letter country code
    * address family (4 or 6)
    * ASN
    * improvement count (predicted cummulative number of AS hops that RIS would come closer to prefixes for that geo area if it were to peer with that network)
