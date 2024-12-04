from __future__ import absolute_import
from importlib import reload

def show():
    from . import orient_dialog, orient, tools
    reload(orient_dialog)
    reload(orient)
    reload(tools)
    w = orient_dialog.ObjectOrientDialog()
    w.show()
    return w
