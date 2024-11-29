from __future__ import absolute_import
from importlib import reload

def show():
    from . import dialog, orient
    reload(dialog)
    reload(orient)
    w = dialog.ObjectOrientDialog()
    w.show()
    return w
