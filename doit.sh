YYYY=2024
MM=07
DD=23

# minimum number of RIS peers that see a prefix (before the prefix is considered 'significant'
THRES=28 

mkdir -p ./data

date
echo "creating peer.pfx.pathlen.$YYYY.$MM.$DD.txt.gz"
if [ ! -f peer.pfx.pathlen.$YYYY.$MM.$DD.txt.gz ]; then
   for RRC in /mnt/ris/rrc??/$YYYY.$MM/bview.$YYYY$MM$DD.0000.gz
   do 
       bgpdump -m -t change $RRC
   done | ./pathlen.py | gzip -9 > ./data/peer.pfx.pathlen.$YYYY.$MM.$DD.txt.gz
fi

### creates a file with
# peers/prefixes (count) (min dist) (max dist)
date
echo "creating stats.$YYYY.$MM.$DD.txt.gz"
if [ ! -f stats.$YYYY.$MM.$DD.txt.gz ]; then
   ./dist-stats.py ./data/peer.pfx.pathlen.$YYYY.$MM.$DD.txt.gz $YYYY-$MM-$DD | gzip -9 > ./data/stats.$YYYY.$MM.$DD.txt.gz
fi

### improvements files has
## address family ASN improvement factor (sum AS-hops per peer)
date
echo "creating improvements.$YYYY.$MM.$DD.txt"
if [ ! -f improvements.$YYYY.$MM.$DD.txt.gz ]; then
   for RRC in /mnt/ris/rrc??/$YYYY.$MM/bview.$YYYY$MM$DD.0000.gz
   do
       bgpdump -m -t change $RRC
   #done | ./calc-dist-improvements.py peer.pfx.pathlen.$YYYY.$MM.$DD.txt.gz stats.$YYYY.$MM.$DD.txt.gz $THRES | gzip -9 > improvements.$YYYY.$MM.$DD.txt.gz
   done | ./calc-dist-improvements.py ./data/peer.pfx.pathlen.$YYYY.$MM.$DD.txt.gz ./data/stats.$YYYY.$MM.$DD.txt.gz $THRES $YYYY-$MM-$DD > ./data/improvements.$YYYY.$MM.$DD.txt
fi
