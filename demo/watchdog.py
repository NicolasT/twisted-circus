import os
import time
import socket

from twisted.python import log
from twisted.application import internet

# TODO *In theory*, this could could block the mainloop
# So, it should be rewritten to use UDP 'in Twisted'.

class CircusWatchdogService(internet.TimerService):
    _pid = None
    _socket = None

    def __init__(self, step, host, port, make_message=None):
        self._host = host
        self._port = port
        self._make_message = make_message or self._default_make_message

        internet.TimerService.__init__(self, step, self.tick)

    def tick(self):
        if self._socket is None:
            self._socket = self._make_socket()

        msg = self._make_message()

        try:
            self._socket.sendto(msg, (self._host, self._port))
        except:
            log.err(None, 'Failed to send watchdog message')

            try:
                self._socket.close()
            except:
                log.err(None, 'Failed to close watchdog socket')

            self._socket = None

    def _make_socket(self):
        return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def _default_make_message(self):
        if not self._pid:
            self._pid = os.getpid()

        msg = '%d;%f' % (self._pid, time.time())

        return msg
