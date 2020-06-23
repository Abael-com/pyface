# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" The implementation of a dialog that allows the user to open/save files etc.
"""

from .constant import OK
from .toolkit import toolkit_object


ColorDialog = toolkit_object("color_dialog:ColorDialog")


def get_color(parent, color, show_alpha=False):
    """ Convenience function that displays a color dialog.

    Paramters
    ---------
    parent : toolkit control
        The parent toolkit control for the modal dialog.
    color : Color or color description
        The initial Color object or a string holding a valid color description.
    show_alpha : bool
        Whether or not to show alpha channel information.

    Returns
    -------
    color : Color or None
        The selected color, or None if the user made no selection.
    """
    dialog = ColorDialog(color=color)
    result = dialog.open()
    if result == OK:
        return dialog.color
    else:
        return None