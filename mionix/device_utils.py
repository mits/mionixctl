
import pyudev
import sys
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(dir_path, "python_hidraw"))
try:
    from python_hidraw import hidraw
except:
    import hidraw


def find_device_path(usb_id, interface_num=0):
    # find the appropriate /dev/hidrawX device
    ctx = pyudev.Context()
    for x in ctx.list_devices(ID_VENDOR_ID=usb_id[0], ID_MODEL_ID=usb_id[1]):
        # ID_USB_INTERFACE_NUM is not an attribute of hidraw devices, so first we find the relevant input device
        # then navigate to its hidraw sibling
        if 'ID_USB_INTERFACE_NUM' in x and int(x['ID_USB_INTERFACE_NUM']) == interface_num and list(x.children):
            raw = next(d for d in x.parent.children if d["SUBSYSTEM"] == "hidraw")
            return raw["DEVNAME"]


def open_hiddevice(hid_id, interface_num=0):
    dev_path = find_device_path(hid_id, interface_num)
    try:
        return hidraw.HIDRaw(open(dev_path, 'w+'))
    except:
        print("\nYou don't have write access to {0}".format(dev_path))
        print("""
        Run this script with sudo or ensure that your user belongs to the
        same group as the device and you have write access.
        """.format(dev_path))
