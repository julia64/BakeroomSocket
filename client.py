# coding=utf-8
from twisted.internet.protocol import Protocol, ClientFactory
from twisted.internet import reactor
import threading
import time
import sys
import datetime


class Echo(Protocol):
    def __init__(self):
        self.connected = False

    def connectionMade(self):
        self.connected = True

    def connectionLost(self, reason):
        self.connected = False

    def dataReceived(self, data):
        print(data.decode("utf-8"))


class EchoClientFactory(ClientFactory):
    def __init__(self):
        self.protocol = None

    def startedConnecting(self, connector):
        print("Start to Connect...")

    def buildProtocol(self, addr):
        print("Connected...")
        self.protocol = Echo()
        return self.protocol

    def clientConnectionLost(self, connector, reason):
        print("Lost connection. Reason: ", reason)

    def clientConnectionFailed(self, connector, reason):
        print("Connection is failed, Reason: ", reason)


bStop = False


def routine(factory):
    while not bStop:
        if factory.protocol and factory.protocol.connected:
            factory.protocol.transport.write("hello, I'm %s %s" % (
                sys.argv[0], datetime.datetime.now()
            ))
            print(sys.argv[0], datetime.datetime.now())
        time.sleep(5)


host = '127.0.0.1'
port = 8000
factory = EchoClientFactory()
reactor.connectTCP(host, port, factory)
threading.Thread(target=routine, args=(factory,)).start()
reactor.run()
bStop = True
