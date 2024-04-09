"""Library - networking modules.

This package resembles 'net' directory of linux's source tree.
It contains networking modules.
"""

from . import (
   basesocket,
   ipv4,
)

# from .basesocket import BaseSocket as basesocket

__all__ = [
   'basesocket',
   'ipv4',
]
