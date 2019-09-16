# Scratch Remote Sensors Protocol Connector  2019-08-13 © naohiro2g

import socket
import struct
import unicodedata
import codecs
import sys


class ScratchRSP:
    """
    Communicate with Scratch via Remote Sensors Protocol
    Remote Sensors Connect at the Scratch should be enabled beforehand.
    """
    def __init__(self):
        self.scratchSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.scratchSock.setblocking(True)           # blocking while connect

    def connect(self, host="localhost", port=42001):
        """ Port should be 42001, but you can change host to connect to."""
        try:
            self.scratchSock.connect((host, port))   # blocking while connect
            self.scratchSock.setblocking(False)      # non-blocking afterwards
        except ConnectionRefusedError as e:
            print("Scratchの接続準備ができていないようです。(in scratch.connect)")
            print("指定されたコンピューター名、IPアドレス[{}]は間違いないですか？".format(host))
            print("あるいは、Scratchが起動していて、遠隔センサー接続が有効になっていることを確認してください。\n")
            print("Scratch seems not ready to connect. (in scratch.connect)")
            print("Is host name, or IP address you specified as [{}] correct?".format(host))
            print("Or check if Scrath 1.4 is running there and Remote Sensors Protocol is enabled.\n")
            # self.close()
            self.__init__()
            return e
        return

    def _send(self, cmd):
        try:
            self.scratchSock.send(struct.pack(">I", self._lenCount(cmd)))
            self.scratchSock.send(bytes(cmd, 'UTF-8'))
            print(self._lenCount(cmd), bytes(cmd, 'UTF-8'))
        except BrokenPipeError as e:
            print("\nScratchとの接続が切れています。 Connection to Scratch is lost.")
            return e
        return

    def _lenCount(self, text):
        count = 0
        for c in text:
            if unicodedata.east_asian_width(c) in 'FWA':
                count += 3
            else:
                count += 1
        return count

    def close(self):
        self.scratchSock.close()

    def broadcast(self, msg):
        """ broadcast a message """
        return self._send('broadcast "' + msg + '"')

    def sensor_update(self, sensor_name, sensor_value):
        return self._send('sensor-update "'
                          + sensor_name + '" "' + sensor_value + '" ')

    def receive(self):
        """
        Read the receiving buffer in non-blocking operation.
        Return ASAP if there is no message in the buffer.
        Read all messages in the buffer and return with rdata.
        Messages are separated by \n, newline marks.
        """
        try:                        # non-blocking
            data = self.scratchSock.recv(2048)
        except socket.error as e:
            # return(e)             # Resource temporarily unavailable error
            return("socket.error")
            return e                # don't wait for data
        except BrokenPipeError as e:
            print("Scratch disconnected?")
            return e                #

        i = 0
        rdata = ""                  # there might be many messages in buffer
        while bool(data[i:i+4]):    # read them while byte count is exist
            count = int(codecs.encode(data[i:i+4], 'hex'), 16)
            print('bytes received: ' + str(count) + ' ', end='')
            i += 4      # skip byte count
            print('<message|' + data[i:i+count].decode('utf-8') + '|EOL>')
            rdata += data[i:i+count].decode('utf-8') + "\n"
            i += count              # head to the next message
        return rdata


if __name__ == '__main__':
    # Launch Scratch and enable Remote Sensors Connection.
    # Then run this code by 'python3 scratchRSP' and
    # see the hello message comes in, and watch the value of sensor 'test'.
    import scratchRSP
    import time
    import sys

    print("\nConnecting to Scratch...\n")
    scratch = scratchRSP.ScratchRSP()

    if not scratch.connect():
        print("Scratch Connected!\n")
        scratch.broadcast("hello Scratch!")
        scratch.sensor_update("test", "True")
        time.sleep(1)
        scratch.sensor_update("test", "False")
    else:
        print("Scratch connection error.")
        scratch.close()
        print("\nbye...")
        sys.exit()

    while True:
        if not scratch.receive():
            break

    scratch.close()
    print("\nbye...")
    sys.exit()
