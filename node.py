import subprocess
import threading
try:
    # python2
    from Tkinter import *
    import tkMessageBox as messagebox
except ImportError:
    #python3
    from tkinter import *
    from tkinter import messagebox



class Node:

    def __init__(self, host, port=61209):
        """
        Takes an ip or FQDN to be able to access host
        through ssh and run a command.
        """
        self.host = str(host)
        self.threads = []

    def run(self, command="uname -a", t=True):
        """
        :param command: The remote command to run through ssh
        :param t: wether the ssh connection has the -t flag
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
        # self.connectButton = Button(self, text="Connect")
        # self.connectButton["command"] = lambda: self.node.connect()
        # self.connectButton.pack(side=LEFT)
        # if self.node.alive:
        #    self.connectButton['state'] = DISABLED

        self.button = Button(self, text="Open System Monitor")
        self.button["command"] = lambda: self.node.run("gnome-system-monitor")
        self.button.pack(side=LEFT)

        Button(self, text="Remove", command=self.my_destroy).pack(side=LEFT)

    def my_destroy(self):
        """
        Custom clean up method to remove this entry
        :return: None
        """
        del self.node
        self.destroy()
