from node import *
from os.path import expanduser
import argparse


def add_host(master):
    """
    Create a windows to add a host and add it to the selection list.
    :param master: a tk object
    :return: None
    """
    window = Toplevel(master)
    window.title("Add Host Window")
    Label(window, text="Host Address or Name").pack(side=LEFT)
    value = StringVar()
    entry = Entry(window, textvariable=value)
    entry.pack(side=LEFT)

    def callback():
        v = entry.get().strip()
        if v != "" and v not in node_entries.keys():
            node_entries[v] = NodeEntry(master, host=v)
        window.destroy()

    def enter_key(event):
        callback()

    button = Button(window, text="OK", command=callback)
    window.bind("<Return>", enter_key)
    button.pack(side=LEFT)
    entry.focus()
    window.mainloop()


def remove_host(master):
    """
    Create a windows to remove a host
    :param master: a tk object
    :return: None
    """
    if len(node_entries) <= 0:
        root = Tk()
        root.withdraw()
        messagebox.showwarning(title="Warning", message="No host to remove")
        root.destroy()
        return
    window = Toplevel(master)
    window.title("Remove Host Window")
    Label(window, text="Select Host: ").pack(side=LEFT)
    value = StringVar()
    options = OptionMenu(window, value, *(node_entries.keys()))
    options.config(width=20)
    options.pack(side=LEFT)
    value.set(list(node_entries.keys())[0])

    def callback():
        v = value.get().strip()
        node_entries[v].destroy()
        del node_entries[v]
        window.destroy()

    def enter_key(event):
        callback()

    button = Button(window, text="OK", command=callback)
    button.pack(side=LEFT)
    window.bind("<Return>", enter_key)
    window.mainloop()


def main():
    mainwindow = Tk(className=" Remote Monitor")
    try:
        # load the hosts from the host file
        with open(hostfile) as f:
            for host in f:
                host = host.strip()
                if host != '' and host not in node_entries.keys():
                    node_entries[host] = NodeEntry(mainwindow, host=host)
    except IOError:
        root = Tk()
        root.withdraw()
        messagebox.showwarning("Error", "Host file not found, looked in " + hostfile)
        root.destroy()

    def a_key(event):
        add_host(mainwindow)

    def r_key(event):
        remove_host(mainwindow)


    Frame(mainwindow).pack()
    mainwindow.focus()
    menu = Menu(mainwindow)
    mainwindow.config(menu=menu)
    action_sub_menu = Menu(menu)
    menu.add_cascade(label="Actions", menu=action_sub_menu)
    action_sub_menu.add_command(label="Add host", command=lambda: add_host(mainwindow))
    action_sub_menu.add_command(label="Remove host", command=lambda: remove_host(mainwindow))
    mainwindow.bind("A", a_key)
    mainwindow.bind("a", a_key)
    mainwindow.bind("R", r_key)
    mainwindow.bind("r", r_key)
    mainwindow.mainloop()


hostfile = expanduser("~") + "/hostfile"
parser = argparse.ArgumentParser(description="Remote Monitor Selection")
parser.add_argument("-f", metavar="hostfile", type=str, default=hostfile,
                    help="default is " + hostfile)
args = parser.parse_args()
hostfile = args.f
node_entries = {}

if __name__ == '__main__':
    main()
