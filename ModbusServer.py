from ModbusServerSocket import ModbusServerSocketHandler
from ModbusWriteMultipleReg import ModbusWriteMultipleReg
import socket
import threading


class ModbusServer:
    def __init__(self, rr):
        self.rr = rr
        self.keepRunning = True
        self.connected = False
        self.thread = ''
        self.socket = ''
        self.start()

    def start(self):
        self.thread = threading.Thread(target=self.runThread, daemon=True)
        self.thread.start()

    def checkSocket(self):
        try:
            self.socket.sendall(b"test")
        except:
            self.connected = False
        else:
            self.connected = True

    def runThread(self):
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # bind the socket to a public host, and a well-known port
        serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serversocket.bind(("192.168.1.122", 5002))
        # become a server socket
        serversocket.listen(5)
        while self.keepRunning:
            # accept connections from outside
            (clientsocket, address) = serversocket.accept()
            self.connected = True
            self.socket = clientsocket
            self.socket.settimeout(.5)

            try:
                data = self.socket.recv(1024)
            except:
                self.connected = False
                self.socket.close()
            else:
                while data:
                    # print("got message " + str(len(data)))
                    mssh = ModbusServerSocketHandler(data)
                    mwm = ModbusWriteMultipleReg(mssh, self.rr)
                    data = ''
                    try:
                        data = self.socket.recv(1024)
                    except:
                        self.connected = False
                        self.socket.close()
                self.socket.close()
