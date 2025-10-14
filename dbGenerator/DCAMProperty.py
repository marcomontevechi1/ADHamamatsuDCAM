from ctypes import c_int32, byref

from dcamapi4 import DCAMPROP_ATTR, DCAMPROP_VALUETEXT, dcamprop_getvaluetext
from dcam import Dcam


class NoSuchProperty(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class DCAMProperty:
    """
    Represents a property.
    """

    idprop: c_int32
    dcam: Dcam
    code: str
    name: str
    attribute: DCAMPROP_ATTR
    support_text: DCAMPROP_VALUETEXT

    def __init__(self, dcam: Dcam, idprop: c_int32):
        self.idprop = idprop
        self.dcam = dcam
        self.code = "0x{:08X}".format(idprop)

        self.name = dcam.prop_getname(idprop)
        self.attribute = dcam.prop_getattr(idprop)
        self.check_name_attr()

        self.support_text = self.initialize_support_text()

    def initialize_support_text(self) -> DCAMPROP_VALUETEXT:
        support_text = DCAMPROP_VALUETEXT()
        support_text.iProp = self.idprop
        support_text.value = self.attribute.valuemin
        support_text.alloctext(256)
        dcamprop_getvaluetext(self.dcam._Dcam__hdcam, byref(support_text))

        return support_text.text.decode()

    def check_name_attr(self):
        if self.name is False:
            raise NoSuchProperty(f"No propname found for idprop {self.idprop}")

        if self.attribute is False:
            raise NoSuchProperty(f"No propattr found for idprop {self.idprop}")
