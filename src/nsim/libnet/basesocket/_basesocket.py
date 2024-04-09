from .flags import Flags as flags
from .descriptors import Descriptors as descriptors

import time
from threading import (
   Event,
   Thread,
)

import nsim as app

class _BaseSocket:
   """BaseSocket object for development and debugging of network algorithms.
   
   Development and debug oriented replacement for built-in socket library,
   meant to be used with nsim's library for developing and debugging network
   algorithms.
   This is the core of nsim project. It mimics built-in socket library to some
   extent, just enough to support algorithm development.
   To add your own algorithms to this, modify the file and include one.
   
   Attributes
   ----------
   _sock_family : int
      Socket address family.
   _sock_type : int
      Socket type.
   _sock_proto : int
      Socket protocol number.
   _layers : list
      List of layer objects attached to the socket.
   _layers_queue_type : list
      List of type of queue buffer supported by layers.
   _layer_names : list
      List of names of each layer attached to the socket.
   _layer_queues : list
      List of queue buffers attached to the socket.
   _layer_queue_bind : dict
      Mapping of queue buffers to participating layers' combined names.
   _layer_queue_names : list
      List of names mapped to queue buffers.
   _ip_destination : int
      IP address of the destination currently connected.
   _port_destination : int
      Port number of the destination currently connected.
   _listen : int
      Number of connections to keep at backlog, while serving.
   _timeout : int
      Timeout value, to be used by various operations.
   _status : int
      Status flag for socket's current state.
   
   Methods
   -------
   __init__ (sock_family, sock_type, sock_proto)
      Init basesocket with specified configurations.
   basesocket ()
      Configures layers and queues for basesocket.
   bind ()
      Binds basesocket to address.
   listen ()
      Enables to accept connections to basesocket.
   accept ()
      Accepts connections to basesocket.
   connect ()
      Connects basesocket to destination address.
   shutdown ()
      Shuts down one or both halves of connection.
   close ()
      Closes basesocket.
   send ()
      Sends data to basesocket.
   sendto ()
      Sends data to specified address via basesocket.
   recv ()
      Receives data from basesocket.
   settimeout ()
      Sets timeout for basesocket operations.
   """
   
   # _BaseSocket internal (but also public facing) lib / functions
   
   def __init__ (
      self,
      
      sock_family   = flags.AF_INET,
      sock_type     = flags.SOCK_DGRAM,
      sock_proto    = flags.SOCK_PROTO_NONE,
   ):
      """Init basesocket with specified configurations.
      
      Parameters
      ----------
      sock_family : int, default=flags.AF_INET
         Socket address family.
      sock_type : int, default=flags.SOCK_DGRAM
         Socket type.
      sock_proto : int, default=flags.SOCK_PROTO_NONE
         Socket protocol number.
      """
      
      self._sock_family       = flags.SOCK_FAMILY_NONE
      self._sock_type         = flags.SOCK_TYPE_NONE
      self._sock_proto        = flags.SOCK_PROTO_NONE
      
      self._layers            = list()
      self._layers_queue_type = list()
      self._layer_names       = list()
      self._layer_queues      = list()
      self._layer_queue_bind  = dict()
      self._layer_queue_names = list()
      
      self._ip_destination    =  0
      self._port_destination  =  1
      
      self._listen            = -1
      self._timeout           = -1
      
      self._status            = flags.STATUS_NONE
      
      self.basesocket(
         sock_family = sock_family,
         sock_type   = sock_type,
         sock_proto  = sock_proto,
      )
   
   def basesocket (
      self,
      sock_family = flags.AF_INET,
      sock_type   = flags.SOCK_DGRAM,
      sock_proto  = flags.SOCK_PROTO_NONE,
   ):
      """Configures layers and queues for basesocket.
      
      Initializes layers and sets queue type for basesocket.
      For customization, add your custom algorithms only in this function.
      
      Parameters
      ----------
      sock_family : int, default=flags.AF_INET
         Socket address family.
      sock_type : int, default=flags.SOCK_DGRAM
         Socket type.
      sock_proto : int, default=flags.SOCK_PROTO_NONE
         Socket protocol number.
      
      Returns
      -------
      bool
         Returns success.
      """
      
      result                = True
      layers                = list()
      layers_queue_type     = list()
      
      if (sock_family      == flags.SOCK_FAMILY_NONE):
         result             = True
      elif (sock_family    == flags.AF_INET):
         from nsim.libnet.ipv4 import protocol
         
         layers.append(protocol.ipv4())
         layers_queue_type.append([list, list])
         
         if (sock_type     == flags.SOCK_TYPE_NONE):
            result          = True
         elif (sock_type   == flags.SOCK_STREAM):
            result          = False
         elif (sock_type   == flags.SOCK_DGRAM):
            from nsim.libnet.ipv4 import simplifiedudp
            
            layers.append(simplifiedudp.simplifiedudp())
            layers_queue_type.append([list, list])
            
            if (sock_proto == flags.SOCK_PROTO_NONE):
               result       = True
            else:
               result       = False
         else:
            result          = False
      else:
         result             = False
      
      if (result):
         self._sock_family = sock_family
         self._sock_type   = sock_type
         self._sock_proto  = sock_proto
         
         layers.reverse()
         layers_queue_type.reverse()
         
         self._layers.clear()
         self._layers_queue_type.clear()
         
         self._layers            = layers
         self._layers_queue_type = layers_queue_type
         
         if (self._layers):
            # this part should come by assessing NIC, but here only
            
            from nsim.libdriver.net import simplifiedslip
            
            self._layers.append(simplifiedslip.simplifiedslip())
            self._layers_queue_type.append([list, bytearray])
         
         self._bind_layers()
         
         self._status = flags.STATUS_OPEN
      else:
         self._status = flags.STATUS_NONE
      
      return result
   
   def _bind_layers (self):
      """Binds layers and queues for basesocket.
      
      Initializes queue buffers for intermediate layers and binds both together
      to the basesocket.
      This is responsible for setting up layers' names and queues' names as
      well.
      
      Returns
      -------
      NoneType
         Returns None.
      """
      
      from nsim.libhardwareinterface import queue
      
      for layer_queue in self._layer_queues:
         layer_queue.clear()
      
      self._layer_queues.clear()
      self._layer_queue_bind.clear()
      
      layers_queue_types = [
         layers_queue_type[0].__name__
         for layers_queue_type in self._layers_queue_type
      ]
      layers_queue_types.append(self._layers_queue_type[-1][1].__name__)
      
      for layers_queue_type in layers_queue_types:
         layers_queue_type = (
            queue.flags.QUEUE_TYPE_BYTE
            if (layers_queue_type == 'bytearray')
            else
            queue.flags.QUEUE_TYPE_NORMAL
         )
         self._layer_queues.append([
            queue.queue(queue_type=layers_queue_type), # up_to_down up_out
            queue.queue(queue_type=layers_queue_type), # down_to_up up_in
         ])
      
      layer_names = [
         str(type(layer).__name__).lower()
         for layer in self._layers
      ]
      
      self._layer_names = (['application'] + layer_names + ['physical'])
      
      layer_names = [
         [
            '.'.join([layer_name_current, layer_name_next]),
            '.'.join([layer_name_next, layer_name_current]),
         ]
         for layer_name_current, layer_name_next in zip(
            (['application'] + layer_names),
            (layer_names + ['physical']),
         )
      ]
      
      self._layer_queue_names = layer_names
      
      if (self._layers):
         self._layers[0].stream(
            stream_up_out   = self._layer_queues[0][0],
            stream_up_in    = self._layer_queues[0][1],
         )
         self._layer_queue_bind[
            layer_names[0][0]
         ] = self._layer_queues[0][0]
         self._layer_queue_bind[
            layer_names[0][1]
         ] = self._layer_queues[0][1]
         
         if (len(self._layers) > 1):
            self._layers[0].stream(
               stream_down_in  = self._layer_queues[1][0],
               stream_down_out = self._layer_queues[1][1],
            )
            self._layer_queue_bind[
               layer_names[1][0]
            ] = self._layer_queues[1][0]
            self._layer_queue_bind[
               layer_names[1][1]
            ] = self._layer_queues[1][1]
      
      for layer_index, layer in enumerate(self._layers[1:-1]):
         layer.stream(
            stream_up_out   = self._layer_queues[layer_index + 1][0],
            stream_up_in    = self._layer_queues[layer_index + 1][1],
            stream_down_in  = self._layer_queues[layer_index + 2][0],
            stream_down_out = self._layer_queues[layer_index + 2][1],
         )
         self._layer_queue_bind[
            layer_names[layer_index + 1][0]
         ] = self._layer_queues[layer_index + 1][0]
         self._layer_queue_bind[
            layer_names[layer_index + 1][1]
         ] = self._layer_queues[layer_index + 1][1]
         
         self._layer_queue_bind[
            layer_names[layer_index + 2][0]
         ] = self._layer_queues[layer_index + 2][0]
         self._layer_queue_bind[
            layer_names[layer_index + 2][1]
         ] = self._layer_queues[layer_index + 2][1]
      
      if (self._layers):
         if (len(self._layers) > 1):
            self._layers[-1].stream(
               stream_up_out   = self._layer_queues[-2][0],
               stream_up_in    = self._layer_queues[-2][1],
            )
            self._layer_queue_bind[
               layer_names[-2][0]
            ] = self._layer_queues[-2][0]
            self._layer_queue_bind[
               layer_names[-2][1]
            ] = self._layer_queues[-2][1]
         
         self._layers[-1].stream(
            stream_down_in  = self._layer_queues[-1][0],
            stream_down_out = self._layer_queues[-1][1],
         )
         self._layer_queue_bind[
            layer_names[-1][0]
         ] = self._layer_queues[-1][0]
         self._layer_queue_bind[
            layer_names[-1][1]
         ] = self._layer_queues[-1][1]
      
      return None
   
   def bind (self, address):
      """Binds basesocket to address.
      
      Binds basesocket to source address and starts progress mechanism.
      
      Parameters
      ----------
      address : tuple
         Tuple containing source address.
      
      Returns
      -------
      NoneType
         Returns None.
      """
      
      if (not (self._status & flags.STATUS_OPEN)):
         return None
      
      if (self._bind_source(address)):
         self._status |= flags.STATUS_BOUND
         
         try:
            self._progress_mechanism.state(
               activate=True,
               errors_raise=True,
            )
         except:
            pass
      
      return None
   
   def listen (self, backlog=0):
      """Enables to accept connections to basesocket.
      
      Enables basesocket to accept connections to it and sets number of
      connections to keep at backlog.
      
      Parameters
      ----------
      backlog : int, default=0
         Number of connections to keep at backlog, while serving.
      
      Returns
      -------
      NoneType
         Returns None.
      """
      
      if (not (self._sock_type & flags.SOCK_STREAM)):
         return None
      
      if (not (
         self._status
         & flags.STATUS_OPEN
         & flags.STATUS_BOUND
      )):
         return None
      
      try:
         backlog = int(backlog)
         
         if (backlog <= 0):
            backlog = 0
      except:
         backlog = -1
      
      if (backlog >= 0):
         self._listen = backlog
         
         try:
            self._progress_mechanism.state(
               activate=True,
               errors_raise=True,
            )
         except:
            pass
      
      return None
   
   def accept (self):
      """Accepts connections to basesocket.
      
      Waits for connection to basesocket, and upon receiving one, accepts and
      returns basesocket.
      Currently, is a stub, and returns self.
      
      Returns
      -------
      object
         Returns basesocket (connection) object.
      NoneType
         Returns None if in invalid state.
      """
      
      if (not (self._sock_type & flags.SOCK_STREAM)):
         return None
      
      if (not (
         self._status
         & flags.STATUS_OPEN
         & flags.STATUS_BOUND
      )):
         return None
      
      if (self._listen < 0):
         return None
      
      return self
   
   def connect (self, address):
      """Connects basesocket to destination address.
      
      Binds basesocket to destination using address specified and starts
      progress mechanism.
      
      Parameters
      ----------
      address : tuple
         Tuple containing destination address.
      
      Returns
      -------
      NoneType
         Returns None.
      """
      
      if (not (self._sock_type & flags.SOCK_STREAM)):
         return None
      
      if (not (
         self._status
         & flags.STATUS_OPEN
         & flags.STATUS_BOUND
      )):
         return None
      
      if (self._bind_destination(address)):
         self._status |= flags.STATUS_CONNECTED
         
         try:
            self._progress_mechanism.state(
               activate=True,
               errors_raise=True,
            )
         except:
            pass
      
      return None
   
   def shutdown (self, how=flags.SHUT_NONE):
      """Shuts down one or both halves of connection.
      
      Shuts down one or both halves of connection.
      Currently a stub.
      
      Parameters
      ----------
      how : int, default=flags.SHUT_NONE
         Method of connection shutdown, send, receive, or both parts.
      
      Returns
      -------
      NoneType
         Returns None.
      """
      
      if (not (self._sock_type & flags.SOCK_STREAM)):
         return None
      
      if (not (
         self._status
         & flags.STATUS_OPEN
         & flags.STATUS_BOUND
         & flags.STATUS_CONNECTED
      )):
         return None
      
      if (how & flags.SHUT_RD):
         self._bind_destination(address=(0,1))
      
      if (how & flags.SHUT_WR):
         pass
      
      if (how & flags.SHUT_RDWR):
         self._status -= (self._status & flags.STATUS_CONNECTED)
      
      return None
   
   def close (self, flag=flags.SHUT_RDWR):
      """Closes basesocket.
      
      Closes basesocket and stops progress mechanism.
      
      Parameters
      ----------
      flag : int, default=flags.SHUT_RDWR
         Flags to mark close methods.
      
      Returns
      -------
      NoneType
         Returns None.
      """
      
      if (not (self._status & flags.STATUS_OPEN)):
         return None
      
      if (flag not in (
         flags.SHUT_RD,
         flags.SHUT_WR,
         flags.SHUT_RDWR,
      )):
         return None
      
      self._status = flags.STATUS_NONE
      
      try:
         self._progress_mechanism.state(
            activate=False,
            errors_raise=True,
         )
      except:
         pass
      
      return None
   
   def _bind_source (self, address):
      """Binds basesocket to source address.
      
      Binds basesocket to source address by iterating over all attached layers
      and calling ip and port methods to set source address.
      
      Parameters
      ----------
      address : tuple
         Tuple containing source address.
      
      Returns
      -------
      bool
         Returns success.
      """
      
      ip = 0 # address[0]
      port = address[1]
      
      result = 0
      
      for layer in self._layers:
         try:
            layer.ip(ip_source=ip)
            result |= 1
         except:
            pass
         
         try:
            layer.port(port_source=port)
            result |= 2
         except:
            pass
      
      return (True if (result & 3) else False)
   
   def _bind_destination (self, address):
      """Binds basesocket to destination address.
      
      Binds basesocket to destination address by iterating over all attached
      layers and calling ip and port methods to set destination address.
      
      Parameters
      ----------
      address : tuple
         Tuple containing destination address.
      
      Returns
      -------
      bool
         Returns success.
      """
      
      ip = 0 # address[0]
      port = address[1]
      
      result = 0
      
      for layer in self._layers:
         try:
            layer.ip(ip_destination=ip)
            self._ip_destination = ip
            result |= 1
         except:
            pass
         
         try:
            layer.port(port_destination=port)
            self._port_destination = port
            result |= 2
         except:
            pass
      
      return (True if (result & 3) else False)
   
   def send (self, data):
      """Sends data to basesocket.
      
      Sends data to basesocket to be sent to connected destination.
      It simply appends data to the initial queue buffer.
      
      Parameters
      ----------
      data : bytes
         Encoded data (bytes) to be sent.
      
      Returns
      -------
      int
         Returns length of data sent.
      """
      
      if (not (self._sock_type & flags.SOCK_STREAM)):
         return -1
      
      if (not (
         self._status
         & flags.STATUS_OPEN
         & flags.STATUS_BOUND
         & flags.STATUS_CONNECTED
      )):
         return -1
      
      data = data[:50000]
      
      try:
         datalength = self._layer_queues[0][0].flow_in(data=[data])
      except:
         datalength = 0
      
      if (datalength):
         return (len(data))
      
      return datalength
   
   def sendto (self, data, address):
      """Sends data to specified address via basesocket.
      
      Sends data to specified address via basesocket. To do so, it first binds
      basesocket to destination address follwed by sending data.
      To send, it simply appends data to the initial queue buffer.
      
      Parameters
      ----------
      data : bytes
         Encoded data (bytes) to be sent.
      address : tuple
         Tuple containing destination address.
      
      Returns
      -------
      int
         Returns length of data sent.
      """
      
      if (not (self._status & flags.STATUS_OPEN)):
         return -1
      
      ip = self._ip_destination
      port = self._port_destination
      
      self._bind_destination(address)
      
      data = data[:50000]
      
      try:
         datalength = self._layer_queues[0][0].flow_in(data=[data])
      except:
         datalength = 0
      
      self._bind_destination((ip, port))
      
      if (datalength):
         return (len(data))
      
      return datalength
   
   def recv (self, bufsize):
      """Receives data from basesocket.
      
      Receives data from basesocket.
      To receive, it simply fetches data from topmost queue buffer.
      It uses timeouts to loop until data or timeout.
      Currently, buffer size (bufsize) is ignored.
      
      Parameters
      ----------
      bufsize : int
         Maximum length of data to be fetched.
      
      Returns
      -------
      bytes
         Returns encoded (or raw) data (bytes).
      """
      
      if (not (self._status & flags.STATUS_OPEN)):
         return b''
      
      _event_timeout_wait   = Event()
      _event_timeout_active = Event()
      _thread_timeout_timer = None
      timeout_interval      = 0.1
      
      if (self._timeout):
         _event_timeout_wait.set()
         _event_timeout_active.set()
         
         def _timeout_timer (
            timeout               = self._timeout,
            timeout_interval      = timeout_interval,
            timeout_step          = 0.1,
            _event_timeout_wait   = _event_timeout_wait,
            _event_timeout_active = _event_timeout_active,
         ):
            if (timeout < 0):
               _event_timeout_active.clear()
               return None
            
            while (
                   (timeout > 0)
               and (_event_timeout_active.wait(timeout=0.0))
            ):
               time.sleep(timeout_interval)
               timeout -= timeout_step
            
            _event_timeout_wait.clear()
            _event_timeout_active.clear()
            
            return None
         
         if (self._timeout > 0):
            _thread_timeout_timer = Thread(
               target = _timeout_timer,
               daemon = True,
            )
            _thread_timeout_timer.start()
      else:
         _event_timeout_wait.clear()
      
      # bufsize is ignored for now as queue is for message, not bytes
      retry = True
      data  = b''
      
      while (retry):
         try:
            data = self._layer_queues[0][1].flow_out(data_length=1)
         except:
            data = b''
         
         if (data or (not _event_timeout_wait.wait(timeout=0.0))):
            retry = False
         else:
            time.sleep(timeout_interval)
      
      _event_timeout_active.clear()
      _event_timeout_wait.clear()
      
      if (_thread_timeout_timer is not None):
         try:
            _thread_timeout_timer.join(timeout=(timeout_interval + 0.1))
         except:
            pass
      
      return data
   
   def settimeout (self, value):
      """Sets timeout for basesocket operations.
      
      Sets timeout for basesocket operations.
      This simply updates _timeout variable.
      
      Parameters
      ----------
      value : int, float, NoneType
         Timeout value (amount), None or negative value for no timeout.
      
      Returns
      -------
      NoneType
         Returns None.
      """
      
      if (not (self._status & flags.STATUS_OPEN)):
         return None
      
      if (value is None):
         value = -1
      
      try:
         value = float(value)
         
         if (value < 0):
            value = -1
      except:
         value = -1
      
      self._timeout = value
      
      return None
