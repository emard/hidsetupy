#!/usr/bin/env python3

# python hid initialization
# a helper script for experimenter to
# find minimal USB setup sequence for
# a HID device to start sending reports

# first, device must be blacklisted to prevent being
# initialized by the kernel driver:

# /etc/udev/rules.d/22-mouse-blacklist.rules
# # Microsoft USB optical mouse blacklist
# SUBSYSTEM=="usb", ATTRS{idVendor}=="045e", ATTRS{idProduct}=="0039", ATTR{authorized}="0"

import usb1
import time
with usb1.USBContext() as context:
    handle = context.openByVendorIDAndProductID(
        0x045e, 0x0039, # microsoft mouse
#        0x046d, 0xc30b, # logitech netplay
        skip_on_error=True,
    )
    if handle is None:
        print("Device not present, or user is not allowed to access device.")
    if handle.kernelDriverActive(0):
        handle.detachKernelDriver(0)
    time.sleep(0.5e-3)
    handle.resetDevice()
    time.sleep(0.5e-3)
    print(handle.controlRead(0x80, 0x06, 0x0100, 0x0000, 0x0040, timeout=20)) # get descriptor len 0x40
    time.sleep(0.5e-3)
    print(handle.controlRead(0x80, 0x06, 0x0100, 0x0000, 0x0012, timeout=20)) # get descriptor len 0x12
    time.sleep(0.5e-3)
    print(handle.controlRead(0x80, 0x06, 0x0200, 0x0000, 0x0009, timeout=20)) # get descriptor len 0x09
    time.sleep(0.5e-3)
    print(handle.controlRead(0x80, 0x06, 0x0200, 0x0000, 0x0022, timeout=20)) # get descriptor len 0x09
    time.sleep(0.5e-3)
    print(handle.controlRead(0x80, 0x06, 0x0300, 0x0000, 0x00FF, timeout=20)) # get descriptor len 0x09
    time.sleep(0.5e-3)
    print(handle.controlRead(0x80, 0x06, 0x0302, 0x0409, 0x00FF, timeout=20)) # get descriptor len 0x09
    time.sleep(0.5e-3)
    print(handle.controlRead(0x80, 0x06, 0x0301, 0x0409, 0x00FF, timeout=20)) # get descriptor len 0x09
    time.sleep(0.5e-3)
    handle.controlWrite(0x00, 0x09, 0x0001, 0x0000, b"", timeout=20) # set configuration 1 -> mouse front LED ON
    time.sleep(0.5e-3)
    try:
      print(handle.controlRead(0x81, 0x06, 0x2200, 0x0000, 0x0048, timeout=50)) # get descriptor len 0x48
    except:
      print("some err")
    print("press buttons/move mouse now")
    time.sleep(1.0)
    for x in range(0,20):
       try:
           print(handle.interruptRead(1,4,timeout=20)) # get report
       except:
           print(x)
           time.sleep(100.0e-3)
