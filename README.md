# Remote Monitor Selection

This program is a simple UI built in python for the purpose of viewing the
system stats of multiple machines. The main role is to allow for the easy opening
of gnome-system-monitor of the desire host remotely. This is dependent of the user
running the programs to have ssh keys setup to the desire host in such a way that
```
$ ssh <host> date
```
response seamlessly and quietly.

The program also has the capability of showing other stats if the remote host is running a glance server 
and are reachable.
The showing of this additional stats are minimal and require improvement such as how much data is being requested
and the time delay between them.

# Running
```
$ python main.py
```

# Dependencies (compatible with both python3 and python2.7)
- socket
- tkinter
- xmlrpc or xmlrpclib
- threading
- subprocess
- argparse

# Optional Dependencies
Have glance2.x or higher running on the remote host in server mode
refer to <a href="https://github.com/nicolargo/glances">Glance Github</a>
