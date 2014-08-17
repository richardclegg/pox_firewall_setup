#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import Controller
from mininet.node import RemoteController
import os                                                                                              


class SingleSwitchTopo(Topo):
    "Single switch connected to n hosts."
    def __init__(self):
        # Initialize topology and default options
        Topo.__init__(self)
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        sf = self.addSwitch('sf')
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 =self.addHost('h3')
        hf = self.addHost('hf');
        l11= self.addLink(h1,s1)
        l22= self.addLink(h2,s2)
        l33= self.addLink(h3,s3)
        lff= self.addLink(hf,sf)
        l12= self.addLink(s1,s2)
        l23= self.addLink(s2,s3)
        l2f= self.addLink(s2,sf)
        
class POXBridge( Controller ):                                                                         
    "Custom Controller class to invoke POX forwarding.l2_learning"                                     
    def start( self ):                                                                                 
        "Start POX learning switch"                                                          
        self.pox = '%s/pox/pox.py' % os.environ[ 'HOME' ]                                              
        self.cmd( self.pox, 'forwarding.firewall &' )                                               
    def stop( self ):                                                                                  
        "Stop POX"                                                                                     
        self.cmd( 'kill %' + self.pox )                                                                

controllers = { 'poxbridge': POXBridge }  

def simpleTest():
    "Create and test a simple network"
    topo = SingleSwitchTopo()
    net = Mininet(topo,controller=POXBridge) 
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
