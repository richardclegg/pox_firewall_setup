#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import Controller
from mininet.node import RemoteController
import os                                                                                              
import time



        
class POXBridge( Controller ):                                                                         
    "Custom Controller class to invoke POX firewall"                                     
    def start( self ):                                                                                 
        "Start POX learning switch"                                                      
        print "Starting external controller"
        self.pox = '%s/pox/pox.py' % os.environ[ 'HOME' ]                                              
        self.cmd( self.pox, 'forwarding.firewall &' )  
        time.sleep(1)    #Make sure it comes up                                          
    def stop( self ):                                                                                  
        "Stop POX"                                                                                     
        self.cmd( 'kill %' + self.pox )                                                                

controllers = { 'poxbridge': POXBridge }  

def simpleTest():
    "Create and test a simple network"
    net = Mininet()
    #c0 = net.addController('c0',POXBridge)
    c0 = net.addController('c0',RemoteController)
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')
    s3 = net.addSwitch('s3')
    s4 = net.addSwitch('s4')
    h1 = net.addHost('h1')
    h2 = net.addHost('h2')
    h3 =net.addHost('h3')
    h4 = net.addHost('h4');
    l11= net.addLink(h1,s1)
    l22= net.addLink(h2,s2)
    l33= net.addLink(h3,s3)
    l44= net.addLink(h4,s4)
    l12= net.addLink(s1,s2)
    l23= net.addLink(s2,s3)
    l2f= net.addLink(s2,s4)
    net.start()
    print "Dumping host connections"
    dumpNodeConnections(net.hosts)
    print "Testing network connectivity"
    net.pingAll()
    CLI(net)
    net.stop()

if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    simpleTest()
