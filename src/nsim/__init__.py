"""Library - network simulator project (nsim).

Package / library for network simulation tools / libraries.
These tools and libraries together allows developers to develop and debug their
network algorithms.
"""

import os
import sys
from pathlib import Path

sys.path.append(os.path.abspath(
   Path(__file__).parent.parent.resolve(),
))

from . import (
   __author__,
   __version__,
   
   libcommon, # common utils
   libdebug, # centralized debugger and tools.
   libdriver, # interface drivers - wireless, slip, transmitter, receiver, etc
   libhardwareinterface, # nic, wire, queue (up / down - stream with in / out)
   libnet, # ipv4 - tcp / udp, basesocket, etc
   libprogress, # trigger system
   libsysmodules, # system module override
)

# Enable to override by default:
libsysmodules.manager.override()

__all__ = [
   '__author__',
   '__version__',
   
   'libcommon',
   'libdebug',
   'libdriver',
   'libhardwareinterface',
   'libnet',
   'libprogress',
   'libsysmodules',
]
