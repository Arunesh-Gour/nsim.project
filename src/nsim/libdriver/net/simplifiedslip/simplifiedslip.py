from .flags import Flags as flags
from .descriptors import Descriptors as descriptors

from threading import (
   Lock,
   Thread,
)

import nsim as app

class SimplifiedSLIP:
   """Simplified version of SLIP (protocol).
   
   Simplified / stub version of SLIP (protocol), used to demonstrate nsim's
   basic functionality.
   Only for demonstration.
   
   Attributes
   ----------
   _byte_rate_stream_down_in : int
      Uplink transfer rate.
   _byte_rate_stream_down_out : int
      Downlink transfer rate.
   _retries : int
      Number of retries to perform before giving up, during byte transfer.
   _stream_up_in : object
      Queue (stream) object, to upper layer, for downlink.
   _stream_up_out : object
      Queue (stream) object, from upper layer, for uplink.
   _stream_down_in : object
      Queue (stream) object, to lower layer, for uplink.
   _stream_down_out : object
      Queue (stream) object, from lower layer, for downlink.
   _data_up_down : bytearray
      Internal uplink buffer.
   _data_down_up : bytearray
      Internal downlink buffer.
   _lock_process_data_up_down : Lock
      Concurrency lock for uplink transfer processing.
   _lock_process_data_down_up : Lock
      Concurrency lock for downlink transfer processing.
   
   Methods
   -------
   __init__ (**link_queues, **link_rate, retries)
      Init an instance of protocol with specified configurations.
   stream ()
      Sets queue (stream) objects for links.
   process ()
      Processes link transfers, threading capable.
   _process_data_up_down ()
      Processes uplink transfer.
   _process_data_down_up ()
      Processes downlink transfer.
   """
   
   # Needs heavy re-work including variable name changes, re-framing structure,
   # api standardization, etc.
   # But, is postponed to main project development, where simplified versions
   # will be overthrown by realistic / standard versions.
   
   def __init__ (
      self,
      
      stream_up_in              = None,
      stream_up_out             = None,
      stream_down_in            = None,
      stream_down_out           = None,
      
      byte_rate_stream_down_in  = 120, # write to downstream
      byte_rate_stream_down_out =  60, # read from downstream
      
      retries                   =  10,
   ):
      """Init an instance of protocol with specified configurations.
      
      Parameters
      ----------
      stream_up_in : object, NoneType, default=None
         Queue (stream) object, to upper layer, for downlink.
      stream_up_out : object, NoneType, default=None
         Queue (stream) object, from upper layer, for uplink.
      stream_down_in : object, NoneType, default=None
         Queue (stream) object, to lower layer, for uplink.
      stream_down_out : object, NoneType, default=None
         Queue (stream) object, from lower layer, for downlink.
      byte_rate_stream_down_in : int, default=120
         Uplink transfer rate.
      byte_rate_stream_down_out : int, default=60
         Downlink transfer rate.
      retries : int, default=10
         Number of retries to perform before giving up, during byte transfer.
      """
      
      self._byte_rate_stream_down_in  = abs(int(byte_rate_stream_down_in))
      self._byte_rate_stream_down_out = abs(int(byte_rate_stream_down_out))
      
      self._retries                   = abs(int(retries))
      
      self._stream_up_in              = None
      self._stream_up_out             = None
      self._stream_down_in            = None
      self._stream_down_out           = None
      
      self._data_up_down              = bytearray()
      self._data_down_up              = bytearray()
      
      self._lock_process_data_up_down = Lock()
      self._lock_process_data_down_up = Lock()
      
      self.stream(
         stream_up_in    = stream_up_in,
         stream_up_out   = stream_up_out,
         stream_down_in  = stream_down_in,
         stream_down_out = stream_down_out,
      )
   
   def stream (
      self,
      stream_up_in    = None,
      stream_up_out   = None,
      stream_down_in  = None,
      stream_down_out = None,
   ):
      """Sets queue (stream) objects for links.
      
      Sets stream objects only if parameter is not None.
      
      Parameters
      ----------
      stream_up_in : object, NoneType, default=None
         Queue (stream) object, to upper layer, for downlink.
      stream_up_out : object, NoneType, default=None
         Queue (stream) object, from upper layer, for uplink.
      stream_down_in : object, NoneType, default=None
         Queue (stream) object, to lower layer, for uplink.
      stream_down_out : object, NoneType, default=None
         Queue (stream) object, from lower layer, for downlink.
      
      Returns
      -------
      NoneType
         Returns None.
      """
      
      if (stream_up_in is not None):
         self._stream_up_in    = stream_up_in
      
      if (stream_up_out is not None):
         self._stream_up_out   = stream_up_out
      
      if (stream_down_in is not None):
         self._stream_down_in  = stream_down_in
      
      if (stream_down_out is not None):
         self._stream_down_out = stream_down_out
      
      return None
   
   def process (
      self,
      non_blocking   = True,
      thread_timeout = None,
   ):
      """Processes link transfers, threading capable.
      
      Enqueues single uplink and downlink transfers if not already queued.
      
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
      
      if (not self._lock_process_data_up_down.locked()):
         active_threads.append(Thread(
            target = self._process_data_up_down,
            daemon = True,
         ))
         active_threads[-1].start()
      
      if (not self._lock_process_data_down_up.locked()):
         active_threads.append(Thread(
            target = self._process_data_down_up,
            daemon = True,
         ))
         active_threads[-1].start()
      
      if (not non_blocking):
         for active_thread in active_threads:
            active_thread.join(timeout=thread_timeout)
      
      return None
   
   def _process_data_up_down (self):
      """Processes uplink transfer.
      
      Performs uplink transfer by storing a message in internal buffer first,
      then by encapsulating data, followed by transfer.
      
      Returns
      -------
      NoneType
         Returns None.
      """
      
      if (
            (not self._stream_up_out)
         or (not self._stream_down_in)
      ):
         return None
      
      self._lock_process_data_up_down.acquire()
      
      try:
         self._process_data_stream_down_in()
         
         if (self._data_up_down):
            return None
         
         data = self._stream_up_out.flow_out(data_length=1)
         
         if (not data):
            return None
         
         data = self._encapsulate(data[0])
         
         self._data_up_down.extend(data)
      finally:
         self._lock_process_data_up_down.release()
      
      return None
   
   def _process_data_stream_down_in (self):
      """Processes uplink transfer from internal buffer.
      
      Processes uplink transfer from internal buffer to uplink queue (stream)
      for lower layer. If queue (stream) is already full, retries set amount
      of times before giving up.
      
      Returns
      -------
      NoneType
         Returns None.
      """
      
      bytes_remaining = self._byte_rate_stream_down_in
      retries         = self._retries
      
      while (
              bytes_remaining
         and  retries
         and (self._data_up_down)
      ):
         data_length         = self._stream_down_in.flow_in(
            data=[self._data_up_down[0]],
         )
         
         if (data_length):
            self._data_up_down.pop(0)
            
            bytes_remaining -= 1
            retries          = self._retries
         else:
            retries         -= 1
      
      return None
   
   def _process_data_down_up (self):
      """Processes downlink transfer.
      
      Performs downlink transfer by storing a packet in internal buffer first,
      then by decapsulating data, followed by transfer.
      
      Returns
      -------
      NoneType
         Returns None.
      """
      
      if (
            (not self._stream_up_in)
         or (not self._stream_down_out)
      ):
         return None
      
      self._lock_process_data_down_up.acquire()
      
      try:
         self._process_data_stream_down_out()
         
         if (
               (not self._data_down_up)
            or (
               int(self._data_down_up[-1]).to_bytes(1, 'big')
               != flags.SPECIAL_END
            )
         ):
            return None
         
         if (self._stream_up_in.state(full=True)):
            return None
         
         data = self._decapsulate(self._data_down_up)
         
         data_length = self._stream_up_in.flow_in(data=[data])
         
         if (not data_length):
            return None
         
         self._data_down_up.clear()
      finally:
         self._lock_process_data_down_up.release()
      
      return None
   
   def _process_data_stream_down_out (self):
      """Processes uplink transfer to internal buffer.
      
      Processes uplink transfer to internal buffer from uplink queue (stream)
      for lower layer. If queue (stream) is already empty, retries set amount
      of times before giving up.
      
      Returns
      -------
      NoneType
         Returns None.
      """
      
      bytes_remaining = self._byte_rate_stream_down_out
      retries         = self._retries
      
      while (
              bytes_remaining
         and  retries
         and (
               (not self._data_down_up)
            or (
               int(self._data_down_up[-1]).to_bytes(1, 'big')
               != flags.SPECIAL_END
            )
         )
      ):
         data                = self._stream_down_out.flow_out(
            data_length=1,
         )
         
         if (data):
            self._data_down_up += data
            
            bytes_remaining -= 1
            retries          = self._retries
         else:
            retries         -= 1
      
      return None
   
   def _encapsulate (
      self,
      data,
   ):
      """Encapsulates uplink data.
      
      Encapsulates uplink data accoring to (simplified) SLIP protocol.
      
      Parameters
      ----------
      data : int, bytearray
      
      Returns
      -------
      bytearray
         Returns encapsulated data.
      """
      
      data = (
         bytearray(int(data).to_bytes(1, 'big'))
         if (type(data).__name__ == 'int')
         else
         data
      ).replace(
         flags.SPECIAL_ESC,
         flags.SPECIAL_ESC_ESC,
      ).replace(
         flags.SPECIAL_END,
         flags.SPECIAL_ESC_END,
      )
      
      data += flags.SPECIAL_END
      
      return data
   
   def _decapsulate (
      self,
      data,
   ):
      """Decapsulates downlink data.
      
      Decapsulates downlink data accoring to (simplified) SLIP protocol.
      
      Parameters
      ----------
      data : int, bytearray
      
      Returns
      -------
      bytearray
         Returns decapsulated data.
      """
      
      data = data[:-1]
      
      data = (
         bytearray(int(data).to_bytes(1, 'big'))
         if (type(data).__name__ == 'int')
         else
         data
      ).replace(
         flags.SPECIAL_ESC_END,
         flags.SPECIAL_END,
      ).replace(
         flags.SPECIAL_ESC_ESC,
         flags.SPECIAL_ESC,
      )
      
      return data
