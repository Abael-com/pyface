#------------------------------------------------------------------------------
# Copyright (c) 2010, Enthought Inc
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD license.

#
# Author: Enthought Inc
# Description: Qt API selector. Can be used to switch between pyQt and PySide
#------------------------------------------------------------------------------

import importlib
import os
import sys

QtAPIs = [
    ('pyside', 'PySide'),
    ('pyqt5', 'PyQt5'),
    ('pyqt', 'PyQt4'),
]

def prepare_pyqt4():
    # Set PySide compatible APIs.
    import sip
    sip.setapi('QDate', 2)
    sip.setapi('QDateTime', 2)
    sip.setapi('QString', 2)
    sip.setapi('QTextStream', 2)
    sip.setapi('QTime', 2)
    sip.setapi('QUrl', 2)
    sip.setapi('QVariant', 2)

qt_api = None

# have we already imported a Qt API?
for api_name, module in QtAPIs:
    if module in sys.modules:
        qt_api = api_name
        break
else:
    # does our environment give us a preferred API?
    qt_api = os.environ.get('QT_API')

# if we have no preference, is a Qt API available? Or fail with ImportError.
if qt_api is None:
    for api_name, module in QtAPIs:
        try:
            importlib.import_module(module)
            qt_api = api_name
            break
        except ImportError:
            continue
        else:
            raise ImportError('Cannot import PySide, PyQt5 or PyQt4')

# otherwise check QT_API value is valid
elif qt_api not in {api_name for api_name, module in QtAPIs}:
    msg = ("Invalid Qt API %r, valid values are: " +
           "'pyside, 'pyqt' or 'pyqt5'") % qt_api
    raise RuntimeError(msg)


if qt_api == 'pyqt':
    # set the PyQt4 APIs
    prepare_pyqt4()
