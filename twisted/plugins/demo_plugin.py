from zope.interface import implements

from twisted.plugin import IPlugin
from twisted.python import usage
from twisted.internet import endpoints
from twisted.application import internet
from twisted.application.service import IServiceMaker

class Options(usage.Options):
    optParameters = [
        ['listen', 'l', None, '`strports` description of listening address']
    ]

    def postOptions(self):
        if self['listen'] is None:
            raise usage.UsageError('Missing `listen` argument')


class DemoServiceMaker(object):
    implements(IServiceMaker, IPlugin)

    tapname = 'demo'
    description = 'Demo service'
    options = Options

    def makeService(self, options):
        # Note: Don't move this to module-level
        from twisted.internet import reactor
        from demo.factory import DemoFactory

        endpoint = endpoints.serverFromString(reactor, options['listen'])
        return internet.StreamServerEndpointService(endpoint, DemoFactory())


serviceMaker = DemoServiceMaker()
