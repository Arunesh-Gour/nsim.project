from nsim.libnet.basesocket import basesocket
from nsim.libnet.basesocket.flags import Flags as flags

class o_socket (flags):
   """Custom socket module, to be used as override to original.
   
   Custom socket module built on nsim's basesocket module.
   This class inherits flags only.
   
   Attributes
   ----------
   modules : dict
      Collection of original modules (with object), which are overridden.
   _GLOBAL_DEFAULT_TIMEOUT : int, default=-1
      Global default timeout flag.
   """
   
   _GLOBAL_DEFAULT_TIMEOUT = -1
   
   class socket (basesocket):
      """Custom socket class for overridden socket module.
      
      Custom socket class built on nsim's basesocket class.
      This class inherits basesocket class.
      
      Methods
      -------
      socket ()
         This is basesocket.basesocket() method, with just name changed.
      """
      
      socket = basesocket.basesocket
