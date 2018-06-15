from node import *

mainwindow = Tk(className=" Remote Monitor Selection")

NodeEntry(mainwindow,  host="pclab23.cs.umb.edu")
NodeEntry(mainwindow, host="pclab25.cs.umb.edu")
NodeEntry(mainwindow, host="pclab24.cs.umb.edu")


mainwindow.minsize(width=350, height=250)
mainwindow.mainloop()
