from threading import (
   Lock,
)

class Debugger:
   """Basic debug utility for basesockets.
   
   Basic but powerful and efficent utility for debugging BaseSocket objects.
   Allows quick debugging of custom algorithms designed using BaseSocket.
   Provides easy access to queues and layers used in BaseSocket.
   
   Attributes
   ----------
   basesocket : BaseSocket
      BaseSocket object to be debugged.
   _lock_operation : Lock()
      Concurrency lock for operation(s) on basesocket.
   
   Methods
   -------
   __init__ (basesocket)
      Init debugger with specified basesocket.
   progress_mechanism ()
      Provides access to basesocket's progress mechanism.
   layers ()
      Provides access to basesocket's layers.
   queues ()
      Provides access to basesocket's queue buffers.
   """
   
   def __init__ (self, basesocket):
      """Init debugger with specified basesocket.
      
      Parameters
      ----------
      basesocket : BaseSocket
         BaseSocket object to be debugged.
      """
      
      self.basesocket = basesocket
      self._lock_operation = Lock()
   
   def progress_mechanism (
      self,
      
      activate       = None,
      get_object     = False,
      
      non_blocking   = False,
      thread_timeout = None,
   ):
      """Provides access to basesocket's progress mechanism.
      
      Provides acces to progress mechanism attached to basesocket and allows
      quick tasks like activation or deactivation.
      
      Parameters
      ----------
      activate : bool, NoneType, default=None
         Alter the state of basesocket's progress mechanism.
      get_object : bool, default=False
         Retrieves progress mechanism object attached with basesocket.
      non_blocking : bool, default=False
         Run current interaction in non-blocking mode ?
      thread_timeout : int, float, NoneType, default=None
         Thread timeout if running in blocking mode.
      
      Returns
      -------
      object
         Returns progress mechanism object attached to basesocket.
      bool
         Returns True on normal interation with progress mechanism's state.
      str
         Returns progress mechanism's type (name) attached to basesocket.
      NoneType
         Returns None if invalid configuration or parameters.
      """
      
      if (not self.basesocket):
         return None
      
      self._lock_operation.acquire()
      
      try:
         if (activate is not None):
            return (self.basesocket._progress_mechanism.state(
               activate       = activate,
               non_blocking   = non_blocking,
               thread_timeout = thread_timeout,
            ))
         elif (get_object):
            return (self.basesocket._progress_mechanism)
         else:
            return (str(type(
               self.basesocket._progress_mechanism
            ).__name__).strip().lower())
      finally:
         self._lock_operation.release()
      
      return None
   
   def layers (
      self,
      name       = '',
      index      = 0,
      get_object = False,
   ):
      """Provides access to basesocket's layers.
      
      Provides access to basesocket's layers and allows fetching individual
      layers based on their name or index.
      
      Parameters
      ----------
      name : str, default=''
         Name of the layer (attached to basesocket) to fetch.
      index : int, default=0
         Index of the layer (attached to basesocket) to fetch.
      get_object : bool, default=False
         Retrieve layer objects attached with basesocket ?
      
      Returns
      -------
      list
         Returns list of details regarding all layers attached to basesocket.
      bool
         Returns True if searched layer is present.
      object
         Returns requested layer object attached to basesocket.
      NoneType
         Returns None if invalid configuration or parameters.
      """
      
      if (not self.basesocket):
         return None
      
      self._lock_operation.acquire()
      
      try:
         name = str(name).strip().lower()
         name = (
            name
            if (
                   (name)
               and (name in self.basesocket._layer_names)
               and (name not in (
                  'application',
                  'physical',
               ))
            )
            else
            ''
         )
         index = (
            0
            if (index < 2)
            else (
               (len(self.basesocket._layer_names) - 2)
               if (index >= (len(self.basesocket._layer_names) - 1))
               else
               (int(index) - 1)
            )
         )
         
         layer_data = None
         
         if (name or index):
            if (name):
               layer_data = self.basesocket._layers[
                  (self.basesocket._layer_names.index(name) - 1)
               ]
            
            if (
                   (index)
               and (not layer_data)
            ):
               layer_data = self.basesocket._layers[
                  (index - 1)
               ]
            
            if (layer_data):
               if (get_object):
                  pass
               else:
                  layer_data = True
            else:
               layer_data = None
         else:
            layer_data = [
               (
                  self.basesocket._layers[
                     (layer_index - 1)
                  ]
                  if (get_object)
                  else (
                     [
                        (layer_index + 1),
                        layer_name,
                     ]
                  )
               )
               for layer_index, layer_name in enumerate(
                  self.basesocket._layer_names
               )
               if (
                     (not get_object)
                  or (
                         (get_object)
                     and (layer_index not in (
                        0,
                        (len(self.basesocket._layer_names) - 1),
                     ))
                  )
               )
            ]
         
         return layer_data
      finally:
         self._lock_operation.release()
      
      return None
   
   def queues (
      self,
      name       = '',
      index      = 0,
      sub_index  = 0,
      state      = False,
      contents   = False,
      get_object = False,
   ):
      """Provides access to basesocket's queue buffers.
      
      Provides access to basesocket's queue buffers and allows fetching
      individual queue buffers and their data based on their name or index
      or index and sub_index. Data can range from queue buffer's state to their
      contents and even queue buffer objects.
      
      Parameters
      ----------
      name : str, default=''
         Name of the queue buffer (attached to basesocket) to fetch.
      index : int, default=0
         Index of the queue buffer set (attached to basesocket) to fetch.
      sub_index : int, default=0
         Sub index in the queue buffer set for the details to be fetched.
      state : bool, default=False
         Retrieve current state of queue buffers attached with basesocket ?
      contents : bool, default=False
         Retrieve contents of queue buffers attached with basesocket ?
      get_object : bool, default=False
         Retrieve queue buffer objects attached with basesocket ?
      
      Returns
      -------
      list
         Returns list of details for all queue buffers attached to basesocket.
      int
         Returns state of searched queue buffer attached to basesocket.
      bool
         Returns True if searched queue buffer is present.
      object
         Returns requested queue buffer object attached to basesocket.
      NoneType
         Returns None if invalid configuration or parameters.
      """
      
      if (not self.basesocket):
         return None
      
      self._lock_operation.acquire()
      
      try:
         name = str(name).strip().lower()
         name = (
            name
            if (
                   (name)
               and (name in self.basesocket._layer_queue_bind.keys())
            )
            else
            ''
         )
         index = (
            0
            if (index < 1)
            else (
               len(self.basesocket._layer_queues)
               if (index >= len(self.basesocket._layer_queues))
               else
               int(index)
            )
         )
         sub_index = (
            0
            if (
                  (not index)
               or (sub_index < 1)
            )
            else (
               len(self.basesocket._layer_queues[0])
               if (sub_index >= len(self.basesocket._layer_queues[0]))
               else
               int(sub_index)
            )
         )
         
         queue_data = None
         
         if (name or index or sub_index):
            if (name):
               queue_data = self.basesocket._layer_queue_bind.get(name)
            
            if (
                   (sub_index)
               and (not queue_data)
            ):
               queue_data = self.basesocket._layer_queues[
                  (    index - 1)
               ][
                  (sub_index - 1)
               ]
            
            if (queue_data):
               if (get_object):
                  pass
               elif (contents):
                  queue_data = (queue_data.contents())
                  # queue_data = (queue_data._queue.copy())
               elif (state):
                  queue_data = (queue_data.state(full=True, value=True))
               else:
                  queue_data = True
            elif (
                   (        index)
               and (not sub_index)
               and (not queue_data)
            ):
               queue_data = self.basesocket._layer_queues[
                  (index - 1)
               ]
               
               if (queue_data):
                  if (get_object):
                     pass
                  elif (contents):
                     queue_data = [
                        (queue.contents())
                        # (queue._queue.copy())
                        for queue in queue_data
                     ]
                  elif (state):
                     queue_data = [
                        (queue.state(full=True, value=True))
                        for queue in queue_data
                     ]
                  else:
                     queue_data = True
               else:
                  queue_data = None
            else:
               queue_data = None
         else:
            queue_data = [
               (
                  [
                     queue[0], # up_down
                     queue[1], # down_up
                  ]
                  if (get_object)
                  else (
                     [
                        queue[0].contents(), # up_down
                        queue[1].contents(), # down_up
                        # queue[0]._queue.copy(), # up_down
                        # queue[1]._queue.copy(), # down_up
                     ]
                     if (contents)
                     else (
                        [
                           queue[0].state(full=True, value=True), # up_down
                           queue[1].state(full=True, value=True), # down_up
                        ]
                        if (state)
                        else (
                           [
                              (queue_index + 1),
                              [  # queue_1
                                 queue_name[0],
                                 [
                                    (queue_index + 1),
                                    1,
                                 ],
                                 [
                                    queue[0].state(full=True, value=True),
                                    queue[0].state(capacity=True),
                                    queue[0].queue_type(describe=True),
                                 ],
                              ],
                              [  # queue_2
                                 queue_name[1],
                                 [
                                    (queue_index + 1),
                                    2,
                                 ],
                                 [
                                    queue[1].state(full=True, value=True),
                                    queue[1].state(capacity=True),
                                    queue[1].queue_type(describe=True),
                                 ],
                              ],
                           ]
                        )
                     )
                  )
               )
               for queue_index, (queue, queue_name) in enumerate(zip(
                  self.basesocket._layer_queues,
                  self.basesocket._layer_queue_names,
               ))
            ]
         
         return queue_data
      finally:
         self._lock_operation.release()
      
      return None
