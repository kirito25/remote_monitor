import subprocess
import threading
from utils import *
import socket
try:
    import xmlrpclib
except ImportError:
    # To run on centOS
    import xmlrpc.client as xmlrpclib
try:
    from Tkinter import *
except ImportError:
    from tkinter import *

socket.setdefaulttimeout(1.0)

class Node:

    def __init__(self, host, port=61209):
        """
        Takes an ip or FQDN to be able to access host
        through ssh and run a command.
        """
        self.host = str(host)
        self.threads = []
        self.connection = None
        self.alive = False
        self.connection = xmlrpclib.ServerProxy('http://' + self.host + ":" + str(port))
        self._connect()

    def connect(self):
        """
        Method to run glances -s on node, not implemented yet
        :return:
        """
        # TODO find way to run glances in server mode from the client
        #self.run("/home/cristian/bin/run_glances", t=False)
        self._connect()

    def _connect(self):
        """
        Preform a xmlrpc server check and update node alive status
        :return: None
        """
        try:
            self.connection.getNow()
            self.alive = True
        except:
            self.alive = False

    def run(self, command="uname -a", t=True):
        """
        :param command: The remote command to run through ssh
        :return: None
        """
        thread = threading.Thread(target=self._run, args=(command, t))
        thread.start()
        self.threads.append(thread)

    def _run(self, command, t=True):
        if t:
            ssh = subprocess.Popen(["ssh", "-t", "-X", "%s" % self.host, command],
                                   shell=False,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        else:
            ssh = subprocess.Popen(["ssh", "-X", "%s" % self.host, command],
                                   shell=False,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)

        ssh.wait()

    def usedRAM(self):
        """
        :return: string of the RAM used
        """
        default = "        N/A"
        if not self.alive:
           return default
        try:
            socket.setdefaulttimeout(1.0)
            return humanReadable(eval(self.connection.getMem())['used'])
        except:
            return default

    def getLoad(self):
        """
        :return: a dictionary, or 'N/A'
            ex {"min1": 0.05, "min5": 0.14, "min15": 0.22}
        """
        if not self.alive:
            return None
        try:
            socket.setdefaulttimeout(1.0)
            loads = eval(self.connection.getLoad())
            del loads['cpucore']
            return loads
        except:
            return None

    def loadStr(self):
        """
        :return: a str of the load as shown on top or 'N/A'
        """
        default = "                  N/A"
        if not self.alive:
            return default
        try:
            return "".join(["%3.2f, " % (i,) for i in self.getLoad().values()]).strip()[:-1]
        except:
            return default


    def isAlive(self):
        """
        Indicator if there is an active connection
        :return: true is connection to node works
        """
        self._connect()
        return self.alive

    def __str__(self):
        return self.host


class NodeEntry(Frame):

    def __init__(self, master, *args, **kwargs):
        host = kwargs['host'].strip()
        Frame.__init__(self, master)
        self.grid(pady=5, padx=5)
        Label(self, text="{:>20}".format(host) + ":").pack(side=LEFT)
        self.node = Node(host)

        # TODO once a remote method of running glance is found uncomment this
        #self.connectButton = Button(self, text="Connect")
        #self.connectButton["command"] = lambda: self.node.connect()
        #self.connectButton.pack(side=LEFT)
        #if self.node.isAlive():
        #    self.connectButton['state'] = DISABLED

        self.button = Button(self, text="Open System Monitor")
        self.button["command"] = lambda: self.node.run("gnome-system-monitor")
        self.button.pack(side=LEFT)

        self.usedRAM = StringVar()
        self.load = StringVar()
        self.setUsedRAM()
        self.setLoad()

        Label(self, textvariable=self.usedRAM).pack(side=LEFT)
        Label(self, textvariable=self.load).pack(side=LEFT)

        self.remove = Button(self, text="Remove")
        self.remove["command"] = lambda: self.my_destroy()
        self.remove.pack(side=LEFT)

        self.updateEntry()

    def updateEntry(self):
        self.node.isAlive()
        # TODO once a remote method of running glance is found uncomment this
        #self.connectButton['state'] = DISABLED if self.node.isAlive() else NORMAL
        self.setLoad()
        self.setUsedRAM()
        self.after(3000, self.updateEntry)

    def setUsedRAM(self):
        self.usedRAM.set("RAM Usage: " + self.node.usedRAM())

    def setLoad(self):
        self.load.set("Load: " + self.node.loadStr())

    def my_destroy(self):
        """
        Custom clean up method to remove this entry
        :return: None
        """
        del self.node
        self.destroy()



