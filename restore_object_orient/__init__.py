from __future__ import absolute_import
from importlib import reload

def show():
    from . import dialog, orient, geo_tools
    reload(dialog)
    reload(orient)
    reload(geo_tools)
    w = dialog.ObjectOrientDialog()
    w.show()
    return w
