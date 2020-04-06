#!/usr/bin/python3
"""Custom topology example

Two directly connected switches plus a host for each switch:

   host --- switch --- switch --- host

Adding the 'topos' dict with a key/value pair to generate our newly defined
topology enables one to pass in '--topo=mytopo' from the command line.
"""

# sudo mn --custom custom_example.py --topo mytopo

import time
import sys

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.link import TCLink

import sys
flush = sys.stdout.flush


class LinuxRouter(Node):
    "A Node with IP forwarding enabled."

    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        # Enable forwarding on the router
        self.cmd('sysctl net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super(LinuxRouter, self).terminate()


class NetworkTopo(Topo):
    "Simple topology example."

    def __init__(self):
        "Create custom topo."

        # Initialize topology
        Topo.__init__(self)

        # topo = self
        # net = Mininet(topo=topo)  # controller is used by s1-s3
        # net.start()
        # info('*** Routing Table on Router:\n')
        # info(net['r0'].cmd('route'))
        # CLI(net)
        # net.stop()

        # Add hosts and switches
        # leftHost = self.addHost('h1')
        # rightHost = self.addHost('h2')
        # leftSwitch = self.addSwitch('s3')
        # rightSwitch = self.addSwitch('s4')

        # create hosts
        # pc1 = self.addHost('pc1')
        # pc2 = self.addHost('pc2')
        # pc3 = self.addHost('pc3')
        # pc4 = self.addHost('pc4')
        # pc5 = self.addHost('pc5')
        # cloud = self.addHost('cloud')

        # start shells
        # pc1.startShell()

        # Add links
        # self.addLink(leftHost, leftSwitch)
        # self.addLink(leftSwitch, rightSwitch)
        # self.addLink(rightSwitch, rightHost)

    def build(self, **_opts):

        defaultIP = '192.168.1.1/24'  # IP address for r0-eth1
        r0 = self.addNode('r0', cls=LinuxRouter, ip=defaultIP)

        # router = self.net.get('r0')
        # for i in range(1,6):
        #     router.setIP('192.168.{}.1/24'.format(i+1), intf='r0-eth{}'.format(i+1))

        # s1, s2, s3 = [self.addSwitch(s) for s in ('s1', 's2', 's3')]

        # self.addLink(s1, router, intfName2='r0-eth1',
        #              params2={'ip': defaultIP})  # for clarity
        # self.addLink(s2, router, intfName2='r0-eth2',
        #              params2={'ip': '172.16.0.1/12'})
        # self.addLink(s3, router, intfName2='r0-eth3',
        #              params2={'ip': '10.0.0.1/8'})

        # h1 = self.addHost('h1', ip='192.168.1.100/24',
        #                   defaultRoute='via 192.168.1.1')
        # h2 = self.addHost('h2', ip='172.16.0.100/12',
        #                   defaultRoute='via 172.16.0.1')
        # h3 = self.addHost('h3', ip='10.0.0.100/8',
        #                   defaultRoute='via 10.0.0.1')

        # ------------------------------ add hosts
        h1 = self.addHost('h1',  ip='192.168.1.100/24',
                          defaultRoute='via 192.168.1.1')
        h2 = self.addHost('h2',  ip='192.168.2.100/24',
                          defaultRoute='via 192.168.2.1')
        h3 = self.addHost('h3',  ip='192.168.3.100/24',
                          defaultRoute='via 192.168.3.1')
        h4 = self.addHost('h4',  ip='192.168.4.100/24',
                          defaultRoute='via 192.168.4.1')
        h5 = self.addHost('h5',  ip='192.168.5.100/24',
                          defaultRoute='via 192.168.5.1')
        cloud = self.addHost('cloud', ip='192.168.0.100/24',
                             defaultRoute='via 192.168.0.1')

        # for h, s in [(h1, s1), (h2, s2), (h3, s3)]:
        #     self.addLink(h, s)

        # ------------------------------- add links
        linkopts = dict(bw=10, delay='2ms', loss=0,
                        max_queue_size=100, use_htb=True)

        for i, link in enumerate([(r0, h1), (r0, h2), (r0, h3), (r0, h4), (r0, h5)]):
            self.addLink(link[0], link[1],
                         intfName1='r0-eth{}'.format(i+1), intfName2='h{}-eth0'.format(i+1),
                         params1={'ip': '192.168.{}.1/24'.format(i+1)},
                         params2={'ip': '192.168.{}.100/24'.format(i+1)},
                         **linkopts
                         )
        self.addLink('r0', 'cloud',
                     intfName1='r0-eth0', intfName2='cloud-eth0',
                     params1={'ip': '192.168.0.1/24'},
                     params2={'ip': '192.168.0.100/24'},
                     bw=100, delay='20ms', loss=0,
                     max_queue_size=1000, use_htb=True
                     )

        # self.addLink(r0, cloud,
        #              params2={'ip': '192.168.0.100/24'})


def setRouterIP(network):
    router = network.get('r0')
    for i in range(1, 5):
        router.setIP('192.168.{}.1/24'.format(i+1),
                     intf='r0-eth{}'.format(i+1))
    router.setIP('192.168.0.1/24',
                 intf='r0-eth0')


def testIperf(network):
    # info('*** Iperf r0 -> h1:\n')
    # src, dst = network.get('r0'), network.get('h1')
    # info("testing", src.name, "<->", dst.name, '\n')
    # src.cmd('telnet', dst.IP(), '5001')
    # serverbw, _clientbw = network.iperf([src, dst], seconds=10)
    # info(serverbw, '\n')

    # info('*** Iperf r0 -> h2:\n')
    # src, dst = network.get('r0'), network.get('h2')
    # info( "testing", src.name, "<->", dst.name, '\n' )
    # src.cmd( 'telnet', dst.IP(), '5001' )
    # serverbw, _clientbw = network.iperf([src, dst], seconds=10)
    # info(serverbw, '\n')

    src, dst = 'r0', 'h1'
    info('*** Iperf {} -> {}\n'.format(src, dst))
    src, dst = network.get(src), network.get(dst)
    dst.cmd('iperf -p 5000 -s -i 1 > /home/mininet/mininet/results/server-{src}-{dst}.txt &'.format(
        src=src.name, dst=dst.name))
    src.cmd('iperf -p 5000 -c 192.168.1.100 -t 10 -i 1 > /home/mininet/mininet/results/client-{src}-{dst}.txt &'.format(
            src=src.name, dst=dst.name))

    src, dst = 'h2', 'h1'
    info('*** Iperf {} -> {}\n'.format(src, dst))
    src, dst = network.get(src), network.get(dst)
    dst.cmd('iperf -p 5001 -s -i 1 > /home/mininet/mininet/results/server-{src}-{dst}.txt &'.format(
        src=src.name, dst=dst.name))
    src.cmd(
        'iperf -p 5001 -c 192.168.1.100 -t 10 -i 1 > /home/mininet/mininet/results/client-{src}-{dst}.txt &'.format(
            src=src.name, dst=dst.name))

    # flush()


def testMgen(network):

    info('*** Mgen test\n')
    # src, dst = 'h2', 'h1'
    # info('*** Mgen {} -> {}\n'.format(src, dst))

    h1, h2 = network.get('h1'), network.get('h2')
    h1.cmd('mgen input /home/mininet/mininet/custom/{name}.mgn output /home/mininet/mininet/results/mgen-{name}.txt &'.format(
        name=h1.name))
    h2.cmd('mgen input /home/mininet/mininet/custom/{name}.mgn output /home/mininet/mininet/results/mgen-{name}.txt &'.format(
        name=h2.name))

    h3 = network.get('h3')
    h3.cmd(
        'mgen input /home/mininet/mininet/custom/{name}.mgn output /home/mininet/mininet/results/mgen-{name}.txt &'.format(name=h3.name))

    h4 = network.get('h4')
    h4.cmd(
        'mgen input /home/mininet/mininet/custom/{name}.mgn output /home/mininet/mininet/results/mgen-{name}.txt &'.format(name=h4.name))

    time.sleep(11.0)
    h1.cmd('pkill mgen')
    h2.cmd('pkill mgen')
    h3.cmd('pkill mgen')
    h4.cmd('pkill mgen')
    # kill all

    # info('*** Test has been finished\n')


def scen1(network, htb=None):
    # scenariusz 1, bez obciazen
    info('*** Scenariusz bez obciazen\n')

    # urzadzenia
    h1 = network.get('h1')
    h2 = network.get('h2')
    h3 = network.get('h3')
    h4 = network.get('h4')
    h5 = network.get('h5')
    r0 = network.get('r0')
    cloud = network.get('cloud')
    hosts = [h1, h2, h3, h4, h5, cloud]

    # wlaczanie htb
    r0.cmd('/home/mininet/mininet/custom/tc_disable.sh')
    if htb is not None:
        r0.cmd('/home/mininet/mininet/custom/{}.sh'.format(htb))

    # uruchomienie mgen, voip
    for host in hosts:
        host.cmd('mgen input /home/mininet/mininet/custom/scen1_{name}.mgn output /home/mininet/mininet/results/scen1_mgen_{name}.txt &'.format(
            name=host.name))

    # http
    httpserver = network.get('cloud')
    httpserver.cmd('python -m SimpleHTTPServer 80 &')
    for host in hosts[:-1]:
        host.cmd(
            'httperf --server 192.168.0.100 --port 80 --wsess=200,3,4 --rate 1 --timeout 10 --hog --verbose > /home/mininet/mininet/results/scen1_httperf_{0}.txt &'.format(host.name))

    # ruch tla tcp
    src, dst = network.get('cloud'), network.get('h1')
    dst.cmd('iperf -p 7000 -s -i 1 > /home/mininet/mininet/results/scen1_iperf_server_{src}_{dst}.txt &'.format(
        src=src.name, dst=dst.name))
    src.cmd('iperf -p 7000 -c 192.168.1.100 -t 300 -i 1 > /home/mininet/mininet/results/scen1_iperf_client_{src}_{dst}.txt &'.format(
            src=src.name, dst=dst.name))

    src, dst = network.get('h3'), network.get('h1')
    dst.cmd('iperf -p 7003 -s -i 1 > /home/mininet/mininet/results/scen1_iperf_server_{src}_{dst}.txt &'.format(
        src=src.name, dst=dst.name))
    src.cmd('iperf -p 7003 -c 192.168.1.100 -t 300 -i 1 > /home/mininet/mininet/results/scen1_iperf_client_{src}_{dst}.txt &'.format(
            src=src.name, dst=dst.name))

    # czekanie na zakonczenie symulacji
    time.sleep(310)

    # wylaczanie mgena
    for host in hosts:
        host.cmd('pkill mgen')
        host.cmd('pkill iperf')
    httpserver.cmd("kill %1")
    r0.cmd('/home/mininet/mininet/custom/tc_disable.sh')


def run(htb=None):
    "Test linux router"
    topo = NetworkTopo()
    net = Mininet(topo=topo, link=TCLink)  # controller is used by s1-s3
    setRouterIP(net)
    net.start()
    info('*** Routing Table on Router:\n')
    info(net['r0'].cmd('route'))

    # testIperf(net)
    # testMgen(net)
    scen1(net, htb)

    CLI(net)
    # net.pingAll()
    net.stop()

# topos = {'networktopo': (lambda: MyTopo())} # te topologie przy uruchamianiu


def without_test():
    "Test linux router"
    topo = NetworkTopo()
    net = Mininet(topo=topo, link=TCLink)  # controller is used by s1-s3
    setRouterIP(net)
    net.start()
    info('*** Routing Table on Router:\n')
    info(net['r0'].cmd('route'))

    CLI(net)
    # net.pingAll()
    net.stop()


topos = {'networktopo': (lambda: NetworkTopo())}

if __name__ == '__main__':
    setLogLevel('info')
    if len(sys.argv) > 2:
        without_test()
    elif len(sys.argv) > 1:
        run(sys.argv[1])
    else:
        run()
