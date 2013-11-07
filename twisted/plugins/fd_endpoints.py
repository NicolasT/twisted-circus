import os
import socket

import ctypes
import ctypes.util

from zope.interface import implements

from twisted.plugin import IPlugin
from twisted.python import log
from twisted.internet import endpoints, interfaces

def make_get_address_family():
    libc = ctypes.CDLL(ctypes.util.find_library('c'), use_errno=True)

    getsockname = libc.getsockname
    # This assumes socklen_t is int
    getsockname.argtypes = \
        [ctypes.c_int, ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)]
    getsockname.restype = ctypes.c_int

    del libc

    af_map = dict(
                (getattr(socket, name), name)
                for name in dir(socket)
                if name.startswith('AF_'))

    def get_address_family(fd):
        log.msg('Resolving address family of FD %d' % fd)

        fd_ = ctypes.c_int(fd)
        addr = ctypes.c_ushort(0)
        len_ = ctypes.c_int(ctypes.sizeof(addr))

        ctypes.set_errno(0)
        res = getsockname(fd_, ctypes.byref(addr), ctypes.byref(len_))

        if res != 0:
            e = ctypes.get_errno()
            raise OSError(e, os.strerror(e))

        af = addr.value

        if af in af_map:
            log.msg('Found address family of FD %d: %s' % (fd, af_map[af]))
        else:
            log.msg('Unknown address family of FD %d: %d' % (fd, af))

        return af

    return get_address_family

get_address_family = make_get_address_family()
del make_get_address_family


class FDServerParser(object):
    implements(IPlugin, interfaces.IStreamServerEndpointStringParser)

    prefix = 'fd'

    def parseStreamServer(self, reactor, *args, **kwargs):
        # Pass to a version with sane arguments
        return self._parseStreamServer(reactor, *args, **kwargs)

    def _parseStreamServer(self, reactor, fd):
        fd = int(fd)

        family = get_address_family(fd)

        return endpoints.AdoptedStreamServerEndpoint(reactor, fd, family)


parser = FDServerParser()
