from twisted.internet import protocol

import demo.protocol

class DemoFactory(protocol.Factory):
    protocol = demo.protocol.DemoProtocol
