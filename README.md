twisted-circus
==============

Demo of a Twisted service running behind a socket managed by Circus.

Requirements
------------
- Python
- Twisted
- *circus* & *circus-web*

Running
-------
For demonstration purposes, a Circus configuration file is provided, see
`demo.ini`. This will launch the Twisted demo service on `127.0.0.1:2323`,
and the *circus-web* interface on `127.0.0.1:8080`.

You can launch everything using

```
$ circusd demo.ini
```

Once the monitor & service processes have been launched (you should get some
Twisted logging in green on your console), you can test the service using

```
$ telnet localhost 2323
```

The service returns a simple message after which it closes the connection.
