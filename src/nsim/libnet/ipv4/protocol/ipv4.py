from .flags import Flags as flags
from .descriptors import Descriptors as descriptors

from threading import (
   Lock,
   Thread,
)

import nsim as app

class IPv4:
   """Simplified version of IPv4.
   
   Stub version of IPv4, used to demonstrate nsim's basic functionality.
   Only for demonstration.
   
   Attributes
   ----------
   _ip_source : int
      Source ip address, to be used.
   _ip_destination : int
      Destination's ip address.
   _retries : int
      Number of retries to perform before giving up, during data transfer.
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
   __init__ (**ip_addresses, **link_queues, retries)
      Init an instance of protocol with specified configurations.
   stream ()
      Sets queue (stream) objects for links.
   ip ()
      Sets ip addresses to be used.
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
      
      ip_source       = 0,
      ip_destination  = 0,
      
      stream_up_in    = None,
      stream_up_out   = None,
      stream_down_in  = None,
      stream_down_out = None,
      
      retries         =  10,
   ):
      """Init an instance of protocol with specified configurations.
      
      Parameters
      ----------
      ip_source : int, default=0
         Source ip address, to be used.
      ip_destination : int, default=0
         Destination's ip address.
      stream_up_in : object, NoneType, default=None
         Queue (stream) object, to upper layer, for downlink.
      stream_up_out : object, NoneType, default=None
         Queue (stream) object, from upper layer, for uplink.
      stream_down_in : object, NoneType, default=None
         Queue (stream) object, to lower layer, for uplink.
      stream_down_out : object, NoneType, default=None
         Queue (stream) object, from lower layer, for downlink.
      retries : int, default=10
         Number of retries to perform before giving up, during data transfer.
      """
      
      self._ip_source                 = 0
      self._ip_destination            = 0
      
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
      
      self.ip(
         ip_source      = ip_source,
         ip_destination = ip_destination,
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
   
   def ip (
      self,
      ip_source      = None,
      ip_destination = None,
   ):
      """Sets ip addresses to be used.
      
      Sets ip addresses only if parameter is not None.
      
      Parameters
      ----------
      ip_source : int, NoneType, default=None
         Source ip address, to be used.
      ip_destination : int, NoneType, default=None
         Destination's ip address.
      
      Returns
      -------
      NoneType
         Returns None.
      """
      
      if (ip_source is not None):
         ip_source            = abs(int(ip_source))
         ip_source            = (
            ip_source
            if (ip_source < 65536)
            else
            0
         )
         self._ip_source      = abs(int(ip_source))
      
      if (ip_destination is not None):
         ip_destination       = abs(int(ip_destination))
         ip_destination       = (
            ip_destination
            if (ip_destination < 65536)
            else
            0
         )
         self._ip_destination = abs(int(ip_destination))
      
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
      
      retries         = self._retries
      
      while (
              retries
         and (self._data_up_down)
      ):
         data_length         = self._stream_down_in.flow_in(
            data=[self._data_up_down.copy()],
         )
         
         if (data_length):
            self._data_up_down.clear()
            
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
         self._process_data_stream_up_in()
         
         if (self._data_down_up):
            return None
         
         data = self._stream_down_out.flow_out(data_length=1)
         
         if (not data):
            return None
         
         data = self._decapsulate(data[0])
         
         self._data_down_up.extend(data)
      finally:
         self._lock_process_data_down_up.release()
      
      return None
   
   def _process_data_stream_up_in (self):
      """Processes downlink transfer from internal buffer.
      
      Processes downlink transfer from internal buffer to downlink queue
      (stream) for upper layer. If queue (stream) is already full, retries set
      amount of times before giving up.
      
      Returns
      -------
      NoneType
         Returns None.
      """
      
      retries         = self._retries
      
      while (
              retries
         and (self._data_down_up)
      ):
         data_length         = self._stream_up_in.flow_in(
            data=[self._data_down_up.copy()],
         )
         
         if (data_length):
            self._data_down_up.clear()
            
            retries          = self._retries
         else:
            retries         -= 1
      
      return None
   
   def _encapsulate (
      self,
      data,
   ):
      """Encapsulates uplink data.
      
      Encapsulates uplink data accoring to (stub) IPv4 (protocol).
      
      Parameters
      ----------
      data : bytearray
      
      Returns
      -------
      bytearray
         Returns encapsulated data.
      """
      
      data = bytearray(b''.join([
         (69).to_bytes(1, 'big'),
         (0).to_bytes(1, 'big'),
         (len(data) + 20).to_bytes(2, 'big'),
         
         (0).to_bytes(4, 'big'),
         
         (8).to_bytes(1, 'big'),
         (17).to_bytes(1, 'big'),
         (0).to_bytes(2, 'big'),
         
         self._ip_source.to_bytes(4, 'big'),
         self._ip_destination.to_bytes(4, 'big'),
         
         data,
      ]))
      
      return data
   
   def _decapsulate (
      self,
      data,
   ):
      """Decapsulates downlink data.
      
      Decapsulates downlink data accoring to (stub) IPv4 (protocol).
      
      Parameters
      ----------
      data : bytearray
      
      Returns
      -------
      bytearray
         Returns decapsulated data.
      """
      
      data = data[((data[0] & 15) * 4):int.from_bytes(data[2:4], 'big')]
      
      return data
