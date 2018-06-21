# Remote Monitor Selection

This program is a simple UI built in python for the purpose of viewing the
system stats of multiple machines. The main role is to allow for the easy opening
of gnome-system-monitor of the desire host remotely. This is dependent of the user
running the programs to have ssh keys setup to the desire host in such a way that
```
$ ssh <host> date
```
response seamlessly and quietly.


# Running
```
$ python main.py
```

# Dependencies (works on python3 and python2.7)
- tkinter
- threading
- subprocess
- argparse

