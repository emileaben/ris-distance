#!/usr/bin/env python3
import sys
import gzip
import socket
import re

## InrdbSocket: communicate with local INRDB instance
class InrdbSocket:
   def __init__( self, sock=None):
      if sock is None:
            self.sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
            self.sock.connect(('inrdb-1.ripe.net', 5555))
            self.recvlines = []
            self.recvbufpart = ''
   def mysend(self, msg):
      ## convenience: make sure msg has \n at the end
      msg = msg.rstrip('\n') + '\n'
      totalsent = 0
      while totalsent < len(msg):
         sent = self.sock.send( str.encode( msg[totalsent:] ) )
         if sent == 0:
            raise RuntimeError("socket connection broken")
         totalsent = totalsent + sent
   def myreceive(self):
      #return self.fd.readline()
      while len( self.recvlines ) == 0:
         chunk = bytes.decode( self.sock.recv(1024) )
         if chunk == '':
            raise IOError("end of file")
         chunk = self.recvbufpart + chunk
         if chunk.rsplit('\n'):
            chunk += '\n'
         self.recvlines = chunk.splitlines()
         self.recvbufpart = self.recvlines.pop()
      ret_line = self.recvlines[0]
      self.recvlines = self.recvlines[1:]
      return ret_line
   def myclose(self):
       self.sock.close()
## end InrdbSocket

class Memoize:
    def __init__(self, fn):
        self.fn = fn
        self.memo = {}

    def __call__(self, *args):
        if args not in self.memo:
            self.memo[args] = self.fn(*args)
        return self.memo[args]

inrdbline_re=re.compile('(BLOB|RES):\s+(.*)')

@Memoize
def find_country( pfx, time_iso ):
   s = InrdbSocket()
   msg = '+dc RIR_STATS %s +xT %s +T +d +M +R\n' % ( pfx, time_iso )
   s.mysend(msg)
   cc = '--'
   while True:
      try:
         line=s.myreceive()
         match = re.match( inrdbline_re, line )
         if match:
            if match.group(1) == 'BLOB':
               cc = match.group(2).split('|')[1]
      except IOError:
            break
   s.myclose()
   #print("pfx as: %s %s" % ( pfx, cc ), file=dfd )
   return cc
