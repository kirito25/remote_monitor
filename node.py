import subprocess
import threading
from utils import *
try:
    # python2
    from Tkinter import *
    import tkMessageBox as messagebox
    import thread
except ImportError:
    #python3
    from tkinter import *
    from tkinter import messagebox
    import _thread as thread


class Node:

    def __init__(self, host):
        """
        Takes an ip or FQDN to be able to access host
        through ssh and run a command.
        """
        self.host = str(host)
        self.threads = []
        self.stop_event = threading.Event()

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
        self.stop_event.wait()
        try:
            ssh.terminate()
        except OSError:
            pass
        thread.exit_thread()

    def kill_threads(self):
        self.stop_event.set()

    def __str__(self):
        if exist(self.host):
            return exist(self.host)
        return self.host + " does not exist"


class NodeEntry(Frame):

    def __init__(self, master, *args, **kwargs):
        host = kwargs['host'].strip()
        Frame.__init__(self, master)
        self.grid(padx=5, pady=5)
        self.node = Node(host)
        button = Button(self, text=self.node.host)
        button["command"] = lambda: self.node.run("gnome-system-monitor")
        if not exist(self.node.host):
            button['state'] = DISABLED
        button.pack(side=LEFT, fill=BOTH)

    def destroy(self):
        """
        Custom clean up method to remove this entry
        :return: None
        """
        self.node.kill_threads()
        Frame.destroy(self)
