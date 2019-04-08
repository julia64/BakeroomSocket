#!/usr/bin/env python
# coding: utf-8

from twisted.internet.protocol import Protocol
from twisted.internet.protocol import Factory
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet import reactor


class Echo(Protocol):

        # 协议类实现用户的服务协议，例如 http,ftp,ssh 等
        def __init__(self, factory):
                self.factory = factory

        def connectionMade(self):

                # 连接建立时被回调的方法

                self.factory.numProtocols = self.factory.numProtocols + 1
                self.transport.write("Welcome! There are currently %d open connections.\n".encode('utf-8')
                                     % self.factory.numProtocols)

        def connectionLost(self, reason):

                # 连接关闭时被回调的方法
                self.factory.numProtocols = self.factory.numProtocols - 1

        def dataReceived(self, data):

                # 接收数据的函数，当有数据到达时被回调
                self.transport.write('00'.encode('utf-8'))


class EchoFactory(Factory):

        #  协议工厂类，当客户端建立连接的时候，创建协议对象，协议对象与客户端连接一一对应
        numProtocols = 0

        def buildProtocol(self, addr):
                return Echo(self)


if __name__ == '__main__':
        # 创建监听端口
        reactor.listenTCP(8007, EchoFactory())

        # 开始监听事件
        reactor.run()
