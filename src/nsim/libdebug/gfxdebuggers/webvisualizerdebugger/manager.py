from nsim.libsysmodules import manager

_overridden = manager.is_overridden()
manager.restore()

from .webservers import genericflaskwebapp
from .webservers.genericflaskwebapp.operations import webserver

if (_overridden):
   manager.override()

socket = manager.module_original('socket')

import time
from threading import (
   Thread,
   Lock,
)

from nsim.libnet.basesocket import basesocket

class Manager:
   """Manager for web visualizer debugger.
   
   Manages operations and working of web visualizer debugger.
   This serves as main interaction point for web visualizer debugger and user.
   
   Attributes
   ----------
   _ip : str
      IP address to bind servers to.
   _port : int
      Port number to bind servers to.
   _default_index : int
      Index of socket to be focussed on, in web visualizer debugger.
   _lock_server_web : Lock
      Concurrency lock for web server.
   _lock_mode : Lock
      Concurrency lock for mode.
   _lock_visualize : Lock
      Concurrency lock for visualization.
   _lock_configuration : Lock
      Concurrency lock for configuration.
   _active : bool
      Debugger's state.
   _active_server_web : bool
      Web visualizer debug server's state.
   _server_web : object
      Web server object for web visualizer debugger.
   
   Methods
   -------
   __init__ (ip, port, **visualization_configuration, **state)
      Init debugger with specified configurations.
   state ()
      Interact with system's state.
   mode ()
      Interact with system's operation mode.
   configuration ()
      Interact with system's configurations.
   visualize ()
      Sets socket to be focussed on in web visualizer debugger.
   start ()
      Starts servers.
   """
   
   def __init__ (
      self,
      
      ip       = '0.0.0.0',
      port     = 5001,
      
      index    = 0,
      socket   = None,
      
      activate = True,
   ):
      """Init debugger with specified configurations.
      
      Parameters
      ----------
      ip : str, default='0.0.0.0'
         IP address to bind servers to.
      port : int, default=5001
         Port number to bind servers to.
      index : int, default=0
         Index of socket to be focussed on, in web visualizer debugger.
      socket : BaseSocket, NoneType, default=None
         BaseSocket object to be focussed on, if index is not known.
      activate : bool, default=True
         Debugger's initial state.
      """
      
      self._ip                  = ''
      self._port                = 5051
      
      self._default_index       = 0
      # self._server_debug        = None
      
      # self._thread_server_web   = None
      # self._thread_server_debug = None
      
      self._lock_server_web     = Lock()
      # self._lock_server_debug   = Lock()
      
      self._lock_mode           = Lock()
      self._lock_visualize      = Lock()
      self._lock_configuration  = Lock()
      
      self._active              = False
      self._active_server_web   = False
      # self._active_server_debug = False
      
      self.configuration(
         ip             = ip,
         port           = port,
         auto_configure = True,
      )
      
      overridden                = manager.is_overridden()
      manager.restore()
      
      self._server_web          = webserver.Executor(
         host  = self._ip,
         port  = self._port,
         debug = False,
      )
      
      if (overridden):
         manager.override()
      
      self.visualize(
         index  = index,
         socket = socket,
      )
      
      self.state(
         activate       = activate,
         non_blocking   = False,
         thread_timeout = None,
      )
   
   def state (
      self,
      
      activate       = None,
      reactivate     = None,
      complete       = False,
      effective      = False,
      detailed       = False,
      
      non_blocking   = True,
      thread_timeout = None,
   ):
      """Interact with system's state.
      
      Parameters
      ----------
      activate : bool, NoneType, default=None
         Set True or False to activate or deactivate system.
      reactivate : bool, NoneType, default=None
         Set True to re-activate system.
      complete : bool, default=False
         Return complete information regarding system's state ?
      effective : bool, default=False
         Return information regarding system's effective state ?
      detailed : bool, default=False
         Return detailed information regarding system's state ?
      non_blocking : bool, default=True
         Run current interaction in non-blocking mode ?
      thread_timeout : int, float, NoneType, default=None
         Thread timeout if running in blocking mode.
      
      Returns
      -------
      bool
         Returns system's active state as requested.
      NoneType
         Returns None on normal run.
      """
      
      if (activate is not None):
         self.mode(
            activate       = bool(activate),
            non_blocking   = non_blocking,
            thread_timeout = thread_timeout,
         )
      elif (reactivate is not None):
         if (self._active):
            self.state(
               activate       = False,
               non_blocking   = non_blocking,
               thread_timeout = thread_timeout,
            )
            
            self.state(
               activate       = True,
               non_blocking   = non_blocking,
               thread_timeout = thread_timeout,
            )
      else:
         if (detailed):
            return (
               self._active,
               self._active_server_web,
               # self._active_server_debug,
            )
         elif (complete):
            return (
                   self._active
               and self._active_server_web
               # and self._active_server_debug
            )
         elif (effective):
            return (
                  self._active
               or self._active_server_web
               # or self._active_server_debug
            )
         else:
            return (self._active)
      
      return None
   
   def mode (
      self,
      activate       = None,
      non_blocking   = True,
      thread_timeout = None,
   ):
      """Interact with system's operation mode.
      
      Parameters
      ----------
      activate : bool, NoneType, default=None
         Set True or False to activate or deactivate system.
      non_blocking : bool, default=True
         Run current interaction in non-blocking mode ?
      thread_timeout : int, float, NoneType, default=None
         Thread timeout if running in blocking mode.
      
      Returns
      -------
      bool
         Returns True.
      """
      
      mode_thread = Thread(
         target = self._modes,
         kwargs = {
            'activate' : activate,
         },
         daemon = False,
      )
      mode_thread.start()
      
      if (mode_thread):
         if (not non_blocking):
            mode_thread.join(timeout=thread_timeout)
      
      return True
   
   def _modes (
      self,
      activate = None,
   ):
      """Switch system's operation mode.
      
      Performs switch operation only if the target mode is not active.
      Can only switch to/from enabled from/to disabled.
      
      Parameters
      ----------
      activate : bool, NoneType, default=None
         Set True or False to activate or deactivate system.
      
      Returns
      -------
      NoneType
         Returns None if invalid parameters.
      bool
         Returns system's state on success.
      """
      
      self._lock_mode.acquire()
      
      try:
         if (activate is not None):
            if (activate != self._active):
               if (not activate):
                  try:
                     self._server_web.stop()
                  except:
                     pass
                  
                  '''
                  try:
                     self._server_debug.stop()
                  except:
                     pass
                  
                  try:
                     self._thread_server_web.join(timeout=0)
                  except:
                     pass
                  
                  try:
                     self._thread_server_debug.join(timeout=0)
                  except:
                     pass
                  '''
                  
                  # self._server_web          = None
                  # self._server_debug        = None
                  # self._thread_server_web   = None
                  # self._thread_server_debug = None
                  
                  self._active              = False
                  self._active_server_web   = False
                  # self._active_server_debug = False
               
               if (activate):
                  '''
                  self._server_web          = webserver.webserver(
                     ip                    = self._ip,
                     port                  = self._port,
                     webvisualizerdebugger = self,
                  )
                  self._server_debug        = debugserver.debugserver(
                     ip   = self._ip,
                     port = (self._port + 1),
                  )
                  
                  self._thread_server_web   = Thread(
                     target = self._start_server_web,
                     daemon = False,
                  )
                  self._thread_server_debug = Thread(
                     target = self._start_server_debug,
                     daemon = True,
                  )
                  '''
                  
                  # web server to be started by user
                  # from main thread !
                  # self._thread_server_web.start()
                  # self._thread_server_debug.start()
                  
                  self._active = True
               
               return (self._active)
            else:
               return (self._active)
         else:
            return None
      except:
         return None
      finally:
         self._lock_mode.release()
      
      return None
   
   def configuration (
      self,
      ip             = None,
      port           = 0,
      auto_configure = False,
   ):
      """Interact with system's configurations.
      
      Parameters
      ----------
      ip : str, NoneType, default=None
         Set IP address to bind servers to.
      port : int, default=0
         Set port number to bind servers to.
      auto_configure : bool, default=False
         Set True to automatically determine some configurations.
      
      Returns
      -------
      tuple
         Returns tuple of system's current configuration.
      NoneType
         Returns None on normal run.
      """
      
      self._lock_configuration.acquire()
      
      try:
         ip = (
            str(ip).strip().lower()
            if (ip is not None)
            else
            None
         )
         
         port = (
            0
            if (
                  (port <   2000)
               or (port >= 36215)
            )
            else
            int(port)
         )
         
         if (ip is not None):
            self._ip = ip
         
         if (port):
            port = self._configure_port(
               port,
               auto_configure=auto_configure,
            )
            
            if (port):
               self._port = port
         
         if (ip or port):
            try:
               self._server_web.host = (
                  self._ip
                  if (self._ip)
                  else
                  '0.0.0.0'
               )
               self._server_web.port = self._port
            except:
               pass
            
            return self.state(
               reactivate=True,
            )
         else:
            return (self._ip, self._port)
      finally:
         self._lock_configuration.release()
      
      return None
   
   def _configure_port (
      self,
      port,
      auto_configure = False,
   ):
      """Determine availability of specified port number.
      
      Opens reusable sockets to determine availability of specified port or
      loops to find next available port if set to auto_configure.
      
      Parameters
      ----------
      port : int, default=0
         Port number to check availability for.
      auto_configure : bool, default=False
         Set True to automatically determine next available port.
      
      Returns
      -------
      int
         Returns available port number on success, else 0.
      """
      
      configured = False
      retries    = 1
      
      if (auto_configure):
         retries = 34214
      
      while (retries):
         retries -= 1
         
         port = (
            2001
            if (
                  (port <=  2000)
               or (port >= 36215)
            )
            else
            int(port)
         )
         
         try:
            socket_test_1 = socket.socket(
               socket.AF_INET,
               socket.SOCK_STREAM,
            )
            socket_test_1.setsockopt(
               socket.SOL_SOCKET,
               socket.SO_REUSEADDR,
               1,
            )
            
            try:
               socket_test_1.bind((
                  self._ip,
                  port,
               ))
            finally:
               try:
                  socket_test_1.shutdown(socket.SHUT_RDWR)
               except:
                  pass
               
               try:
                  socket_test_1.close()
               except:
                  pass
            
            configured = True
         except:
            configured = False
         
         if (configured):
            retries = 0
            break
         else:
            port += 1
      
      if (configured):
         return port
      
      return 0
   
   def visualize (
      self,
      index  = 0,
      socket = None,
   ):
      """Sets socket to be focussed on in web visualizer debugger.
      
      Focuses on the socket to be visualized in web visualizer debugger based
      on either the index or the basesocket object itself.
      
      Parameters
      ----------
      index : int, default=0
         Index of socket to be focussed on, in web visualizer debugger.
      socket : BaseSocket, NoneType, default=None
         BaseSocket object to be focussed on, if index is not known.
      
      Returns
      -------
      bool
         Returns success.
      NoneType
         Returns None if invalid parameters.
      """
      
      self._lock_visualize.acquire()
      
      try:
         index = (
            0
            if (index < 1)
            else (
               len(basesocket.basesocket_objects)
               if (index >= len(basesocket.basesocket_objects))
               else
               int(index)
            )
         )
         
         if (socket):
            if (socket in basesocket.basesocket_objects):
               index = (basesocket.basesocket_objects.index(socket) + 1)
            elif (isinstance(socket, basesocket)):
               basesocket.basesocket_objects.append(socket)
               
               index = (basesocket.basesocket_objects.index(socket) + 1)
            
         if (index):
            self._default_index = index
            
            try:
               genericflaskwebapp.backend.functionality.uapi.debugger._visualize(
                  index=self._default_index,
               )
            except:
               pass
            
            return True
         
         return False
      finally:
         self._lock_visualize.release()
      
      return None
   
   def start (
      self,
   ):
      """Starts servers.
      
      Starts servers.
      This should be called from main thread in most cases.
      Server ran from this method can be closed only by KeyboardInterrupt
      by the user.
      This call is blocking.
      
      Raises
      ------
      Exception
         Exceptions are raised if and as occurred.
      
      Returns
      -------
      object
         Returns object returned by server, after execution.
      NoneType
         Returns None if invalid parameters or configuration.
      """
      
      if (
            (not self._active)
         or (self._lock_server_web.locked())
      ):
         return None
      
      self._lock_server_web.acquire()
      
      try:
         self._active_server_web = True
         
         overridden = manager.is_overridden()
         manager.restore()
         
         if (overridden):
            def auto_remove_override (*args, manager=manager, **kwargs):
               time.sleep(0.8)
               
               manager.override()
               
               return None
            
            Thread(
               target=auto_remove_override,
               daemon=True,
            ).start()
         
         return (self._server_web.start())
      finally:
         try:
            self._active_server_web = False
         except:
            pass
         
         self._lock_server_web.release()
      
      return None
