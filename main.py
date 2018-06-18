from node import *
from os.path import expanduser
import argparse

hostfile = expanduser("~") + "/hostfile"
parser = argparse.ArgumentParser(description="Remote Monitor Selection")
parser.add_argument("-f", metavar="hostfile", type=str, default=hostfile,
                    help="default is " + hostfile)
args = parser.parse_args()
hostfile = args.f
hosts = []
try:
    # load the hosts from the host file
    with open(hostfile) as f:
        for host in f:
            if host.strip() != '':
                hosts.append(host.strip())
except IOError:
    window = Tk(className=" Error")
    Label(window, text="Host file not found, looked in " + hostfile).pack()
    window.mainloop()

def addHost(master):
    """
    Create a windows to add a host and add it to the selection list.
    :param master: a tk object
    :return: None
    """
    window = Tk(className=" Add Host Window")
    Label(window, text="Host Address or Name").pack(side=LEFT)
    value = StringVar()
    entry = Entry(window, textvariable=value)
    entry.pack(side=LEFT)

    def callback():
        v = entry.get().strip()
        if v != "":
            NodeEntry(master, host=str(v))
        window.destroy()

    button = Button(window, text="OK", command=callback)
    button.pack(side=LEFT)
    entry.focus()
    window.mainloop()


def main():
    mainwindow = Tk(className=" Remote Monitor Selection")
    Button(mainwindow, text="Add Host", command=lambda: addHost(mainwindow)).grid(pady=10)
    if len(hosts) > 0:
        for i in hosts:
            NodeEntry(mainwindow, host=str(i))
    # Button to add an entry to the running window
    mainwindow.minsize(width=350, height=250)
    mainwindow.mainloop()


if __name__ == '__main__':
    main()