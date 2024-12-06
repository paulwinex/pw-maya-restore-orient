from __future__ import absolute_import
from importlib import reload

__version__ = '0.0.1'


def show():
    from . import orient_dialog, orient, tools
    reload(orient_dialog)
    reload(orient)
    reload(tools)
    w = orient_dialog.ObjectOrientDialog()
    w.show()
    return w
