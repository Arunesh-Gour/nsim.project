from threading import (
   Thread,
   Lock,
)

class DoubleEndedDirectConnector:
   """Double Ended Direct Connector (DEDC).
   
   Double Ended Direct Connector (DEDC) directly connects two sockets or ends
   using queue streams and allows direct data flow between them.
   
   Attributes
   ----------
   _byte_rate_stream_end_1_end_2 : int
      End_1 -> end_2 link transfer rate.
   _byte_rate_stream_end_2_end_1 : int
      End_2 -> end_1 link transfer rate.
   _retries : int
      Number of retries to perform before giving up, during byte transfer.
   _socket_1 : object
      Socket (BaseSocket) object for end_1 if connecting with sockets.
   _socket_2 : object
      Socket (BaseSocket) object for end_2 if connecting with sockets.
   _identifier_socket_1 : str, NoneType
      Identifier for notification callback bound with end_1's socket.
   _identifier_socket_2 : str, NoneType
      Identifier for notification callback bound with end_2's socket.
   _stream_end_1_in : object
      Queue (stream) object, to end_1, for end_2 -> end_1 link.
   _stream_end_1_out : object
      Queue (stream) object, from end_1, for end_1 -> end_2 link.
   _stream_end_2_in : object
      Queue (stream) object, to end_2, for end_1 -> end_2 link.
   _stream_end_2_out : object
      Queue (stream) object, from end_2, for end_2 -> end_1 link.
   _data_end_1_end_2 : bytearray
      Internal end_1 -> end_2 link buffer.
   _data_end_2_end_1 : bytearray
      Internal end_2 -> end_1 link buffer.
   _lock_process_data_end_1_end_2 : Lock
      Concurrency lock for end_1 -> end_2 link transfer processing.
   _lock_process_data_end_2_end_1 : Lock
      Concurrency lock for end_2 -> end_1 link transfer processing.
   _active_link_end_1_end_2 : bool
      Active state for end_1 -> end_2 link.
   _active_link_end_2_end_1 : bool
      Active state for end_2 -> end_1 link.
   
   Methods
   -------
   __init__ (**sockets, **link_queues, **link_state, **link_rate, retries)
      Init connector and activate links with specified configurations.
   link ()
      Interact with links' states.
   sockets ()
      Sets or unsets socket (BaseSocket) objects for (end) links.
   stream ()
      Sets queue (stream) objects for links.
   process ()
      Processes link transfers, threading capable.
   _process_data_end_1_end_2 ()
      Processes end_1 -> end_2 link transfer.
   _process_data_end_2_end_1 ()
      Processes end_2 -> end_1 link transfer.
   """
   
   def __init__ (
      self,
      
      socket_1                     = None,
      socket_2                     = None,
      
      stream_end_1_in              = None,
      stream_end_1_out             = None,
      stream_end_2_in              = None,
      stream_end_2_out             = None,
      
      activate_link_end_1_end_2    = True, # end_1 -> end_2 link
      activate_link_end_2_end_1    = True, # end_2 -> end_1 link
      
      byte_rate_stream_end_1_end_2 = 240,  # end_1 -> end_2 link
      byte_rate_stream_end_2_end_1 = 240,  # end_2 -> end_1 link
      
      retries                      =  10,
   ):
      """Init connector and activate links with specified configurations.
      
      Parameters
      ----------
      socket_1 : object, NoneType, default=None
         Socket (BaseSocket) object for end_1 if connecting with sockets.
      socket_2 : object, NoneType, default=None
         Socket (BaseSocket) object for end_2 if connecting with sockets.
      stream_end_1_in : object, NoneType, default=None
         Queue (stream) object, to end_1, for end_2 -> end_1 link.
      stream_end_1_out : object, NoneType, default=None
         Queue (stream) object, from end_1, for end_1 -> end_2 link.
      stream_end_2_in : object, NoneType, default=None
         Queue (stream) object, to end_2, for end_1 -> end_2 link.
      stream_end_2_out : object, NoneType, default=None
         Queue (stream) object, from end_2, for end_2 -> end_1 link.
      activate_link_end_1_end_2 : bool, default=True
         Set True or False to activate or deactivate end_1 -> end_2 link.
      activate_link_end_2_end_1 : bool, default=True
         Set True or False to activate or deactivate end_2 -> end_1 link.
      byte_rate_stream_end_1_end_2 : int, default=240
         End_1 -> end_2 link transfer rate.
      byte_rate_stream_end_2_end_1 : int, default=240
         End_2 -> end_1 link transfer rate.
      retries : int, default=10
         Number of retries to perform before giving up, during byte transfer.
      """
      
      self._byte_rate_stream_end_1_end_2  = abs(int(
         byte_rate_stream_end_1_end_2
      ))
      self._byte_rate_stream_end_2_end_1  = abs(int(
         byte_rate_stream_end_2_end_1
      ))
      
      self._retries                       = abs(int(retries))
      
      self._socket_1                      = None
      self._socket_2                      = None
      
      self._identifier_socket_1           = None
      self._identifier_socket_2           = None
      
      self._stream_end_1_in               = None
      self._stream_end_1_out              = None
      self._stream_end_2_in               = None
      self._stream_end_2_out              = None
      
      self._data_end_1_end_2              = bytearray()
      self._data_end_2_end_1              = bytearray()
      
      self._lock_process_data_end_1_end_2 = Lock()
      self._lock_process_data_end_2_end_1 = Lock()
      
      self._active_link_end_1_end_2       = True
      self._active_link_end_2_end_1       = True
      
      self.link (
         activate_link_end_1_end_2 = activate_link_end_1_end_2,
         activate_link_end_2_end_1 = activate_link_end_2_end_1,
      )
      
      self.sockets(
         socket_1 = socket_1,
         socket_2 = socket_2,
      )
      
      self.stream(
         stream_end_1_in  = stream_end_1_in,
         stream_end_1_out = stream_end_1_out,
         stream_end_2_in  = stream_end_2_in,
         stream_end_2_out = stream_end_2_out,
      )
   
   def link (
      self,
      activate_link_end_1_end_2 = None, # end_1 -> end_2 link
      activate_link_end_2_end_1 = None, # end_2 -> end_1 link
   ):
      """Interact with links' states.
      
      Activates or deactivates links only if parameter is not None.
      
      Parameters
      ----------
      activate_link_end_1_end_2 : bool, NoneType, default=None
         Set True or False to activate or deactivate end_1 -> end_2 link.
      activate_link_end_2_end_1 : bool, NoneType, default=None
         Set True or False to activate or deactivate end_2 -> end_1 link.
      
      Returns
      -------
      NoneType
         Returns None.
      """
      
      if (activate_link_end_1_end_2 is not None):
         self._active_link_end_1_end_2 = bool(activate_link_end_1_end_2)
      
      if (activate_link_end_2_end_1 is not None):
         self._active_link_end_2_end_1 = bool(activate_link_end_2_end_1)
      
      return None
   
   def sockets (
      self,
      socket_1 = None,
      socket_2 = None,
   ):
      """Sets or unsets socket (BaseSocket) objects for (end) links.
      
      Sets or unsets socket objects only if parameter is not None.
      Unsets only if parameters are False.
      Also clears notification alerts set with corresponding sockets.
      
      Parameters
      ----------
      socket_1 : object, bool, NoneType, default=None
         Socket (BaseSocket) object for end_1, else False to unset.
      socket_2 : object, bool, NoneType, default=None
         Socket (BaseSocket) object for end_2, else False to unset.
      
      Returns
      -------
      NoneType
         Returns None.
      """
      
      if (socket_1 is not None):
         if (
                self._socket_1
            and self._identifier_socket_1
         ):
            self._socket_1.ProgressionSystem.notification_alert(
               self._socket_1,
               identifier=self._identifier_socket_1,
               unregister=True,
            )
            
            self._socket_1            = None
            self._identifier_socket_1 = None
         
         if (socket_1 is not False):
            self._socket_1 = socket_1
            
            self.stream(
               stream_end_1_out = socket_1._layer_queues[-1][0],
               stream_end_1_in  = socket_1._layer_queues[-1][1],
            )
            
            self._identifier_socket_1 = (
               self._socket_1.ProgressionSystem.notification_alert(
                  self._socket_1,
                  callback = self._callback_notification,
                  times    = -1,
            ))
      
      if (socket_2 is not None):
         if (
                self._socket_2
            and self._identifier_socket_2
         ):
            self._socket_2.ProgressionSystem.notification_alert(
               self._socket_1,
               identifier=self._identifier_socket_2,
               unregister=True,
            )
            
            self._socket_2            = None
            self._identifier_socket_2 = None
         
         if (socket_2 is not False):
            self._socket_2 = socket_2
            
            self.stream(
               stream_end_2_out = socket_2._layer_queues[-1][0],
               stream_end_2_in  = socket_2._layer_queues[-1][1],
            )
            
            self._identifier_socket_2 = (
               self._socket_2.ProgressionSystem.notification_alert(
                  self._socket_2,
                  callback = self._callback_notification,
                  times    = -1,
            ))
      
      return None
   
   def stream (
      self,
      stream_end_1_in  = None,
      stream_end_1_out = None,
      stream_end_2_in  = None,
      stream_end_2_out = None,
   ):
      """Sets queue (stream) objects for links.
      
      Sets stream objects only if parameter is not None.
      
      Parameters
      ----------
      stream_end_1_in : object, NoneType, default=None
         Queue (stream) object, to end_1, for end_2 -> end_1 link.
      stream_end_1_out : object, NoneType, default=None
         Queue (stream) object, from end_1, for end_1 -> end_2 link.
      stream_end_2_in : object, NoneType, default=None
         Queue (stream) object, to end_2, for end_1 -> end_2 link.
      stream_end_2_out : object, NoneType, default=None
         Queue (stream) object, from end_2, for end_2 -> end_1 link.
      
      Returns
      -------
      NoneType
         Returns None.
      """
      
      if (stream_end_1_in is not None):
         self._stream_end_1_in  = stream_end_1_in
      
      if (stream_end_1_out is not None):
         self._stream_end_1_out = stream_end_1_out
      
      if (stream_end_2_in is not None):
         self._stream_end_2_in  = stream_end_2_in
      
      if (stream_end_2_out is not None):
         self._stream_end_2_out = stream_end_2_out
      
      return None
   
   def _callback_notification (
      self,
       *args,
      **kwargs,
   ):
      """Receive point (callback) for notification alerts.
      
      Since automated transfers between sockets depends on either sockets'
      progress, the DEDC depends on their progress mechanism's notifications.
      This is acheived by linking process call with either or both sockets'
      progress mechanism. The alerts are received here, which calls own process
      mechanism to enqueue link transfers.
      
      Returns
      -------
      NoneType
         Returns None.
      """
      
      return (self.process(
         non_blocking=True,
      ))
   
   def process (
      self,
      non_blocking   = True,
      thread_timeout = None,
   ):
      """Processes link transfers, threading capable.
      
      Enqueues single end_1 -> end_2 and end_2 -> end_1 link transfers if not
      already queued.
      
      Parameters
      ----------
      non_blocking : bool, default=True
         Run transfers in non-blocking mode ?
      thread_timeout : int, float, NoneType, default=None
         Thread timeout if running in blocking mode.
      
      Returns
      -------
      NoneType
         Returns None.
      """
      
      active_threads = list()
      
      if (
             (self._active_link_end_1_end_2)
         and (not self._lock_process_data_end_1_end_2.locked())
      ):
         active_threads.append(Thread(
            target = self._process_data_end_1_end_2,
            daemon = True,
         ))
         active_threads[-1].start()
      
      if (
             (self._active_link_end_2_end_1)
         and (not self._lock_process_data_end_2_end_1.locked())
      ):
         active_threads.append(Thread(
            target = self._process_data_end_2_end_1,
            daemon = True,
         ))
         active_threads[-1].start()
      
      if (not non_blocking):
         for active_thread in active_threads:
            active_thread.join(timeout=thread_timeout)
      
      return None
   
   def _process_data_end_1_end_2 (self):
      """Processes end_1 -> end_2 link transfer.
      
      Performs end_1 -> end_2 link transfer by storing bytes from end_1 into
      internal buffer followed by transfer to end_2.
      
      Returns
      -------
      NoneType
         Returns None.
      """
      
      if (
            (not self._active_link_end_1_end_2)
         or (not self._stream_end_1_out)
         or (not self._stream_end_2_in)
      ):
         return None
      
      self._lock_process_data_end_1_end_2.acquire()
      
      try:
         self._process_data_stream_end_1_out()
         
         if (not self._data_end_1_end_2):
            return None
         
         if (self._stream_end_2_in.state(full=True)):
            return None
         
         self._process_data_stream_end_2_in()
      finally:
         self._lock_process_data_end_1_end_2.release()
      
      return None
   
   def _process_data_stream_end_1_out (self):
      """Processes end_1 -> end_2 link transfer to internal buffer.
      
      Processes end_1 -> end_2 link transfer to internal buffer from end_1 link
      queue (stream). If queue (stream) is already empty, retries set amount
      of times before giving up.
      
      Returns
      -------
      NoneType
         Returns None.
      """
      
      bytes_remaining = self._byte_rate_stream_end_1_end_2
      retries         = self._retries
      
      while (
              bytes_remaining
         and  retries
         and (
               (not self._data_end_1_end_2)
            or (
                 len(self._data_end_1_end_2)
               < self._byte_rate_stream_end_1_end_2
            )
         )
      ):
         data                       = self._stream_end_1_out.flow_out(
            data_length=1,
         )
         
         if (data):
            self._data_end_1_end_2 += data
            
            bytes_remaining        -= 1
            retries                 = self._retries
         else:
            retries                -= 1
      
      return None
   
   def _process_data_stream_end_2_in (self):
      """Processes end_1 -> end_2 link transfer from internal buffer.
      
      Processes end_1 -> end_2 link transfer from internal buffer to end_2 link
      queue (stream). If queue (stream) is already full, retries set amount
      of times before giving up.
      
      Returns
      -------
      NoneType
         Returns None.
      """
      
      bytes_remaining = self._byte_rate_stream_end_1_end_2
      retries         = self._retries
      
      while (
              bytes_remaining
         and  retries
         and (self._data_end_1_end_2)
      ):
         data_length         = self._stream_end_2_in.flow_in(
            data=[self._data_end_1_end_2[0]],
         )
         
         if (data_length):
            self._data_end_1_end_2.pop(0)
            
            bytes_remaining -= 1
            retries          = self._retries
         else:
            retries         -= 1
      
      return None
   
   def _process_data_end_2_end_1 (self):
      """Processes end_2 -> end_1 link transfer.
      
      Performs end_2 -> end_1 link transfer by storing bytes from end_2 into
      internal buffer followed by transfer to end_1.
      
      Returns
      -------
      NoneType
         Returns None.
      """
      
      if (
            (not self._active_link_end_2_end_1)
         or (not self._stream_end_1_in)
         or (not self._stream_end_2_out)
      ):
         return None
      
      self._lock_process_data_end_2_end_1.acquire()
      
      try:
         self._process_data_stream_end_2_out()
         
         if (not self._data_end_2_end_1):
            return None
         
         if (self._stream_end_1_in.state(full=True)):
            return None
         
         self._process_data_stream_end_1_in()
      finally:
         self._lock_process_data_end_2_end_1.release()
      
      return None
   
   def _process_data_stream_end_2_out (self):
      """Processes end_2 -> end_1 link transfer to internal buffer.
      
      Processes end_2 -> end_1 link transfer to internal buffer from end_2 link
      queue (stream). If queue (stream) is already empty, retries set amount
      of times before giving up.
      
      Returns
      -------
      NoneType
         Returns None.
      """
      
      bytes_remaining = self._byte_rate_stream_end_2_end_1
      retries         = self._retries
      
      while (
              bytes_remaining
         and  retries
         and (
               (not self._data_end_2_end_1)
            or (
                 len(self._data_end_2_end_1)
               < self._byte_rate_stream_end_2_end_1
            )
         )
      ):
         data                       = self._stream_end_2_out.flow_out(
            data_length=1,
         )
         
         if (data):
            self._data_end_2_end_1 += data
            
            bytes_remaining        -= 1
            retries                 = self._retries
         else:
            retries                -= 1
      
      return None
   
   def _process_data_stream_end_1_in (self):
      """Processes end_2 -> end_1 link transfer from internal buffer.
      
      Processes end_2 -> end_1 link transfer from internal buffer to end_1 link
      queue (stream). If queue (stream) is already full, retries set amount
      of times before giving up.
      
      Returns
      -------
      NoneType
         Returns None.
      """
      
      bytes_remaining = self._byte_rate_stream_end_2_end_1
      retries         = self._retries
      
      while (
              bytes_remaining
         and  retries
         and (self._data_end_2_end_1)
      ):
         data_length         = self._stream_end_1_in.flow_in(
            data=[self._data_end_2_end_1[0]],
         )
         
         if (data_length):
            self._data_end_2_end_1.pop(0)
            
            bytes_remaining -= 1
            retries          = self._retries
         else:
            retries         -= 1
      
      return None
