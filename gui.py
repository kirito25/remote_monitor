from node import *

mainwindow = Tk(className=" Remote Monitor Selection")

NodeEntry(mainwindow,  host="127.0.0.1")
NodeEntry(mainwindow,  host="10.0.0.12")


mainwindow.minsize(width=350, height=250)
mainwindow.mainloop()
