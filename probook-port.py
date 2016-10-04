#!/usr/bin/python
import socket
from threading import Thread
import os
import subprocess

"""class io_port: <-- work in progress
    def __init__(self):
        self.__port = open("/dev/port", "rw")

    def _write_ec(self, register, data):
        self._outb(0x81, 0x66)
        self._outb(register, 0x62)
        self._outb(data, 0x62)

    def _outb(self, x1, x2):
        if(x1 > 0xFF):
            print "em, there is an error here"
            return
"""

class Command:
    def __init__(self):
        pass

    def _call(self,cmd):
        pipe = subprocess.Popen(["perl", "./probook_ec.pl"]+cmd)

class FanOff(Command):
    def execute(self):
        self._call(["FANOFF"])

class SetFan(Command):
    def execute(self, speed):
        self._call([":=", "0x2F", speed])

class Service:
    def _send(self, data) :
        self._socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        self._socket.sendto(data, self._name)

    def __init__(self, name):
        try:
            
            os.unlink(name)
        except:
            pass

        self._name = name

        self._socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        self._socket.bind(self._name)

        os.chmod(self._name, 0777)

        while True:
            data, _ = self._socket.recvfrom(1024)
            print "%s received: '%s'" % (self._name, data)

            if data == "fanoff":
                f=FanOff()
                f.execute()
            elif data[0:6] == "setfan":
                speed = data[7:]
                f = SetFan()
                f.execute(speed)

def main():
    """p = io_port()
    p.write_ec(0x22,1);
    p.write_ec(0x26,0x1F);
    p.write_ec(0x2F,0xFF);"""

    service = Service("/tmp/probook-socket")

if __name__ == "__main__" :
    main()