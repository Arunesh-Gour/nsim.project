"""Library - overriding (system) modules.

This package contains custom modules to override system modules and used as a
replacement to control environment as per nsim's needs.
"""

from .o_socket import o_socket

__all__ = [
   'o_socket',
]
