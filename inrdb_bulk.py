#!/usr/bin/env python

# Simple generic wrapper script to perform INRDB bulk queries

import argparse
import socket
import sys
import time

class MySocket:
    def __init__(self,host,port):
        self.buffer = ''
        self.host = host;
        self.port = int(port);
        #create an INET, STREAMing socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
             self.sock.connect((self.host, self.port))
        except:
             if self.sock:
                self.sock.close()
             print >>sys.stderr, "Could not open socket %s:%d - %s" % (self.host, self.port, message)
             sys.exit(1)
        self.SendLine("-k")
        ack = self.ReceiveLine()
        if ack != "OK":
            raise RuntimeError("unexpected result to -k: " + ack)
        #else:
            #print "socket initialized"

    def SendLine(self, msg):
        line = msg + '\n'
        totalsent = 0
        while totalsent < len(line):
#            print "send(" + line[totalsent:] + ")"
            sent = self.sock.send( str.encode( line[totalsent:] ) )
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent
#            print "%s bytes send" % totalsent
#        print "send done" 

    def ReceiveLine(self):
        index = self.buffer.find("\n")
        if index == -1:
            # no new line, but potentially still some bytes in buffer
            # we still have data from previous call
            line = self.buffer
            newline = 0;
        else:
            line = ''
            chunk = self.buffer
            newline = 1
#            print "buffered chunk: >>" + chunk + "<<"

        while not newline:
            chunk = bytes.decode( self.sock.recv(8192) )
#            print "chunk: >>" + chunk + "<<"
            if chunk == '':
                raise RuntimeError("socket connection broken")
            index = chunk.find("\n")
            if index == -1:
                    line += chunk
#                print line
            else:
                newline = 1

        line += chunk[0:index]
        self.buffer = chunk[index+1:len(chunk)]

#        print "received line: >>" + line + "<<"
#        print "buffered: >>" + self.buffer + "<<"
        return line

    def Close(self):
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-e','--echo', help="echo the INRDB commands to output",action="store_true",default=False)
    parser.add_argument('-p','--port', help="port to send queries to (default 5555)",default=5555)
    parser.add_argument('-i','--inrdbhost', help="host to send queries to (default 'guru')",default="guru.ripe.net")
    parser.add_argument('file',help="file with INRDB queries to be answered")
    args = parser.parse_args()

    commands = open(args.file,'r')



    inrdbSock = MySocket(args.inrdbhost, args.port)
    t1 = time.time()
    for line in commands:
#        cmd = line.rstrip('\n')
        ip = line.rstrip()
        cmd = "+dc RIS_RIB_V +ds aggr +xT 2018-12-14 +M +T " + ip
#        if args.echo:
#            print cmd
        inrdbSock.SendLine(cmd)
        finished = 0
        orig = ''
        while not finished:
                answer = inrdbSock.ReceiveLine()
                if answer != "":
                        try:
                                asn = answer.split('|')[3]
                                if orig:
                                        orig = orig + '|' + asn
                                else:        
                                        orig = asn
                        except:
                                pass
#                    print answer
                if answer[0:9] == "Finished:":
                    print( ip, orig )
                    finished = 1

    t2 = time.time() 
    print( args.inrdbhost, args.port, "elapsed:",int(t2-t1),"seconds" )

#                
    inrdbSock.Close()


