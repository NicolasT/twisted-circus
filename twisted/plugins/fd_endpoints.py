import socket

from zope.interface import implements

from twisted.plugin import IPlugin
from twisted.internet import endpoints, interfaces

class FDServerParser(object):
    implements(IPlugin, interfaces.IStreamServerEndpointStringParser)

    prefix = 'fd'

    def parseStreamServer(self, reactor, *args, **kwargs):
        # Pass to a version with sane arguments
        return self._parseStreamServer(reactor, *args, **kwargs)

    def _parseStreamServer(self, reactor, fd, addressFamily):
        fd = int(fd)

        try:
            family = getattr(socket, addressFamily)
        except AttributeError:
            raise ValueError('Unknown address family: \'%s\'' % addressFamily)

        return endpoints.AdoptedStreamServerEndpoint(reactor, fd, family)


parser = FDServerParser()
