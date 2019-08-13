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
#    if handle.is_kernel_driver_active(INTERFACE) is True:
#        print("Kernel driver active.")
#    #if handle.kernelDriverActive(0):
#    #    handle.detachKernelDriver(0)
#    time.sleep(0.1)
    #handle.claimInterface(0)
    handle.resetDevice()
#    time.sleep(0.1)
    #  time.sleep(0.5e-3)
    #handle.controlWrite(0x00, 0x09, 0, 0, b"", timeout=20) # mouse LED off
    print(handle.controlRead(0x80, 0x00, 0x0000, 0x0000, 0x0002, timeout=20)) # get status
    print(handle.controlRead(0x80, 0x06, 0x0100, 0x0000, 0x12, timeout=20)) # get descriptor len 0x12
    print(handle.controlRead(0x80, 0x06, 0x0300, 0x0000, 0xFF, timeout=20)) # get descriptor len 0x12
    #print(handle.controlRead(0x80, 0x06, 0x0200, 0x0000, 0x09, timeout=20)) # get descriptor len 0x09
    #print(handle.controlRead(0x80, 0x06, 0x0200, 0x0000, 0x22, timeout=20)) # get descriptor len 0x22
    #handle.controlWrite(0x00, 0x01, 0x0001, 0x0000, b"", timeout=20) # clear feature 1
    #print(handle.controlRead(0x80, 0x00, 0x0000, 0x0000, 0x0002, timeout=20)) # get status
    #print(handle.controlRead(0x80, 0x06, 0x0200, 0x0000, 0x22, timeout=20)) # get descriptor len 0x22
    #time.sleep(0.5e-3)
    handle.controlWrite(0x00, 0x09, 0x0001, 0x0000, b"", timeout=20) # set configuration 1 -> mouse front LED ON
    print(handle.controlRead(0x80, 0x08, 0x0000, 0x0000, 0x0001, timeout=20)) # get configuration 1 -> mouse front LED ON
    handle.controlWrite(0x00, 0x03, 0x0001, 0x0000, b"", timeout=20) # set feature 1
    handle.controlWrite(0x00, 0x01, 0x0001, 0x0000, b"", timeout=20) # clear feature 1
    #handle.controlWrite(0x02, 0x01, 0x0001, 0x0000, b"", timeout=20) # clear feature 1 of endpoint
    #print(handle.controlRead(0x82, 0x00, 0x0000, 0x0001, 0x0002, timeout=20)) # get endpoint 1 status
    #print(handle.controlRead(0x82, 0x12, 0x0000, 0x0000, 0x0002, timeout=20)) # get endpoint 1 status
    #print(handle.controlRead(0x80, 0x0A, 0x0001, 0x0000, 0x0001, timeout=20)) # get interface
    #print(handle.controlRead(0x80, 0x06, 0x0200, 0x0000, 0x42, timeout=20)) # get descriptor len 0x09
    #### this will creash: handle.controlWrite(0x00, 0x05, 0x1234, 0x0000, b"", timeout=20) # set address 1234
    #handle.controlWrite(0x21, 0x0A, 0x0001, 0x0000, b"", timeout=20) # set idle 0
    #handle.controlWrite(0x21, 0x09, 0x0201, 0x0000, b"", timeout=20) # set protocol 0x200 error
    #handle.controlWrite(0x21, 0x09, 0x0200, 0x0000, b"\x00", timeout=20) # set protocol 0x200 error
    print("press now")
    time.sleep(0.1)
    for x in range(0,20):
       try:
           print(handle.interruptRead(1,4,timeout=20)) # get report
       except:
           print(x)
           time.sleep(0.1)
