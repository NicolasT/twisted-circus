from zope.interface import implements

from twisted.plugin import IPlugin
from twisted.python import usage
from twisted.internet import endpoints
from twisted.application import internet, service
from twisted.application.service import IServiceMaker

class Options(usage.Options):
    optParameters = [
        ['listen', 'l', None, '`strports` description of listening address'],
        ['watchdog', 'w', None, 'address of circus watchdog (host:port)']
    ]

    def postOptions(self):
        if self['listen'] is None:
            raise usage.UsageError('Missing `listen` argument')

        if self['watchdog']:
            if ':' not in self['watchdog']:
                raise usage.UsageError('Invalid `watchdog` argument format')


class DemoServiceMaker(object):
    implements(IServiceMaker, IPlugin)

    tapname = 'demo'
    description = 'Demo service'
    options = Options

    def makeService(self, options):
        # Note: Don't move this to module-level
        from twisted.internet import reactor
        from demo.factory import DemoFactory
        from demo.watchdog import CircusWatchdogService

        multi = service.MultiService()

        # 'Server' service
        endpoint = endpoints.serverFromString(reactor, options['listen'])
        server = internet.StreamServerEndpointService(endpoint, DemoFactory())
        server.setServiceParent(multi)

        if options['watchdog']:
            addr, port = options['watchdog'].split(':')
            port = int(port)

            watchdog = CircusWatchdogService(1, addr, port)

            watchdog.setServiceParent(multi)

        return multi


serviceMaker = DemoServiceMaker()
