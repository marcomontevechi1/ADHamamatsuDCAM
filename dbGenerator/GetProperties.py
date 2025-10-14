"""Sample script for showing the list of properties with dcam.py.

This script recognizes the camera and shows the list of properties with dcam.py.
Displays the property IDs and values that the camera supported.

This sample source code just shows how to use DCAM-API.
The performance is not guranteed.
"""

__date__ = "2021-06-18"
__copyright__ = "Copyright (C) 2021-2024 Hamamatsu Photonics K.K."

import atexit
from typing import List

from DCAMProperty import DCAMProperty
from dcam import *

# control DCAM functions


def open_device(iDevice=0) -> Dcam:
    """
    Tries to open device.

    Args:
            iDevice (int): Device index.

    Returns:
            Dcam object if success, None if fail.
    """

    if Dcamapi.init():
        atexit.register(Dcamapi.uninit)
        dcam = Dcam(iDevice)
        if dcam.dev_open():
            atexit.register(dcam.dev_close)
            return dcam
        else:
            print("-NG: Dcam.dev_open() fails with error {}".format(dcam.lasterr()))
    else:
        print("-NG: Dcamapi.init() fails with error {}".format(Dcamapi.lasterr()))

    return False


def get_properties(dcam: Dcam) -> List[DCAMProperty]:
    """
    Returns:
            List of DCAMProperty for all properties of device.
    """
    ret = list()
    idprop = dcam.prop_getnextid(0)
    while idprop is not False:
        ret.append(DCAMProperty(dcam, idprop))
        idprop = dcam.prop_getnextid(idprop)

    return ret


def dcam_show_properties(iDevice=0):
    """Show the list of properties.

    Show the list of property IDs and values that the camera supported.

    Args:
            iDevice (int): Device index.

    Returns:
            Nothing.
    """

    dcam = open_device(iDevice)
    if dcam is not None:
        properties = get_properties(dcam)

if __name__ == "__main__":
    dcam_show_properties()
