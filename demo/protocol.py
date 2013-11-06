import os

from twisted.internet import protocol

class DemoProtocol(protocol.Protocol):
    MESSAGE = 'Hello, world! %d\n' % os.getpid()

    def connectionMade(self):
        self.transport.write(self.MESSAGE)
        self.transport.loseConnection()
