from __future__ import absolute_import


def show():
    from . import dialog
    reload(dialog)
    w = dialog.ObjectOrientDialog()
    w.show()
    return w
