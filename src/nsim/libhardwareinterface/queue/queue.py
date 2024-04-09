from .flags import Flags as flags
from .descriptors import Descriptors as descriptors

from threading import (
   Lock,
   Thread,
)

import nsim as app

class Queue:
   """Multi-purpose queue buffer.
   
   Multi-purpose queue buffer system, designed to be used as intermediate
   buffers between layers and protocols to hold data, while providing api
   for monitoring and debugging.
   
   Attributes
   ----------
   _capacity : int
      Queue buffer capacity.
   _queue_type : int
      Queue's buffer type.
   _lock_queue : Lock()
      Concurrency lock for _queue.
   _queue : list, bytearray, NoneType
      Queue buffer store.
   
   Methods
   -------
   __init__ (queue_type, capacity)
      Init queue buffer with specified configuration.
   queue_type ()
      Interact with queue's buffer type.
   state ()
      Query queue buffer's state.
   clear ()
      Clear or empty queue buffer.
   contents ()
      Retrieve contents of queue buffer without deleting them.
   flow_in ()
      Push data into queue buffer.
   flow_out ()
      Retrieve data from queue buffer.
   """
   
   def __init__ (
      self,
      queue_type = flags.QUEUE_TYPE_NORMAL,
      capacity   = -1, # un-limited
   ):
      """Init queue buffer with specified configuration.
      
      Parameters
      ----------
      queue_type : int, default=flags.QUEUE_TYPE_NORMAL
         Queue's buffer type.
      capacity : int, default=-1
         Queue buffer capacity.
      
      Raises
      ------
      Exception
         *  Invalid capacity.
         *  Invalid queue_type.
      """
      
      self._capacity   = int(capacity)
      
      self._queue_type = flags.QUEUE_TYPE_NONE
      
      self._lock_queue = Lock()
      
      self._queue      = None
      
      if (not self._capacity):
         raise Exception((
                 '{0}:\n'
               + 'capacity: {1}\n'
            ).format(
               descriptors.ERROR_CAPACITY_INVALID,
               self._capacity,
            )
         )
      elif (not self._queue_types(
         queue_type=queue_type,
      )):
         raise Exception((
                 '{0}:\n'
               + 'queue_type: {1}\n'
            ).format(
               descriptors.QUEUE_TYPE_SET_FAILURE,
               queue_type,
            )
         )
   
   def queue_type (
      self,
      queue_type     = None,
      non_blocking   = False,
      thread_timeout = None,
      describe       = True,
   ):
      """Interact with queue's buffer type.
      
      Parameters
      ----------
      queue_type : int, NoneType, default=None
         Set queue's buffer type.
      non_blocking : bool, default=False
         Run current interaction in non-blocking mode ?
      thread_timeout : int, float, NoneType, default=None
         Thread timeout if running in blocking mode.
      describe : bool, default=True
         Describe queue's buffer type using descriptors ?
      
      Returns
      -------
      int
         Returns queue's buffer type.
      str
         Returns description of queue's buffer type.
      bool
         Returns True on normal run.
      """
      
      if (queue_type not in (
         flags.QUEUE_TYPE_NONE,
         flags.QUEUE_TYPE_NORMAL,
         flags.QUEUE_TYPE_BYTE,
      )):
         queue_type = None
      
      queue_type_threads = list()
      
      if (queue_type is not None):
         if (
                (      queue_type != flags.QUEUE_TYPE_NONE)
            and (self._queue_type != flags.QUEUE_TYPE_NONE)
         ):
            queue_type_threads.append(Thread(
               target = self._queue_types,
               kwargs = {
                  'queue_type' : flags.QUEUE_TYPE_NONE,
               },
               daemon = True,
            ))
            queue_type_threads[-1].start()
         
         queue_type_threads.append(Thread(
            target = self._queue_types,
            kwargs = {
               'queue_type' : queue_type,
            },
            daemon = True,
         ))
         queue_type_threads[-1].start()
      else:
         queue_type       = self._queue_type
         
         if (describe):
            if (queue_type   & flags.QUEUE_TYPE_NONE):
               queue_type = descriptors.QUEUE_TYPE_NONE
            elif (queue_type & flags.QUEUE_TYPE_NORMAL):
               queue_type = descriptors.QUEUE_TYPE_NORMAL
            elif (queue_type & flags.QUEUE_TYPE_BYTE):
               queue_type = descriptors.QUEUE_TYPE_BYTE
            else:
               queue_type = descriptors.QUEUE_TYPE_SET_UNSET
         elif (queue_type is None):
            queue_type    = descriptors.QUEUE_TYPE_NONE
         
         return queue_type
      
      if (not non_blocking):
         for queue_type_thread in queue_type_threads:
            queue_type_thread.join(timeout=thread_timeout)
      
      return True
      
   def _queue_types (
      self,
      queue_type=flags.QUEUE_TYPE_NONE,
   ):
      """Switch queue's buffer type.
      
      Performs switch operation only if the target buffer type is not same as
      current. Can only switch to/from QUEUE_TYPE_NONE to any other type.
      
      Parameters
      ----------
      queue_type : int, NoneType, default=flags.QUEUE_TYPE_NONE
         Queue's buffer type, to switch to.
      
      Returns
      -------
      bool
         Returns switch's success.
      """
      
      self._lock_queue.acquire()
      
      try:
         if (queue_type not in (
            flags.QUEUE_TYPE_NONE,
            flags.QUEUE_TYPE_NORMAL,
            flags.QUEUE_TYPE_BYTE,
         )):
            return False
         elif (queue_type          != self._queue_type):
            if (queue_type         == flags.QUEUE_TYPE_NONE):
               try:
                  self._queue.clear()
               except:
                  pass
               
               self._queue    = None
            elif (self._queue_type != flags.QUEUE_TYPE_NONE):
               return False
            elif (self._queue_type == flags.QUEUE_TYPE_NONE):
               if (queue_type & flags.QUEUE_TYPE_NORMAL):
                  self._queue = list()
               
               if (queue_type & flags.QUEUE_TYPE_BYTE):
                  self._queue = bytearray()
            
            self._queue_type = queue_type
      finally:
         self._lock_queue.release()
      
      return True
   
   def state (
      self,
      capacity = False,
      empty    = False,
      full     = False,
      relative = False,
      value    = False,
   ):
      """Query queue buffer's state.
      
      Query queue buffer's current state such as capacity, empty or full.
      Reports answers to queries only for set parameters.
      
      Parameters
      ----------
      capacity : bool, default=False
         Report buffer capacity ?
      empty : bool, default=False
         Report whether buffer is empty ?
      full : bool, default=False
         Report whether buffer is full ?
      relative : bool, default=False
         Report respective queries with respect to their alternative extremes.
      value : bool, default=False
         Report respective queries with exact value.
      
      Returns
      -------
      int
         Returns answer to queries as value.
      bool
         Returns answer to queries as True or False.
      NoneType
         Returns None for invalid parameters.
      """
      
      result = None
      
      self._lock_queue.acquire()
      
      try:
         len_queue          = len(self._queue)
         remaining_capacity = self._capacity - len_queue
         
         if (capacity):
            result = (
               -1
               if (self._capacity < 0)
               else
               int(self._capacity)
            )
         elif (empty):
            if (value):
               result = remaining_capacity
            elif (relative):
               result = (
                  True
                  if (remaining_capacity)
                  else
                  False
               )
            else:
               result = (
                  True
                  if (not len_queue)
                  else
                  False
               )
         elif (full):
            if (value):
               result = len_queue
            elif (relative):
               result = (
                  True
                  if (len_queue)
                  else
                  False
               )
            else:
               result = (
                  True
                  if (not remaining_capacity)
                  else
                  False
               )
         elif (value):
            result = 0
         else:
            result = None
      finally:
         self._lock_queue.release()
      
      return result
   
   def clear (self):
      """Clear or empty queue buffer.
      
      Returns
      -------
      bool
         Returns True.
      """
      
      self._lock_queue.acquire()
      
      try:
         if (self._queue_type == flags.QUEUE_TYPE_NONE):
            return True
         else:
            self._queue_type.clear()
      finally:
         self._lock_queue.release()
      
      return True
   
   def contents (self):
      """Retrieve contents of queue buffer without deleting them.
      
      Clones queue buffer's contents and returns them without deleting.
      
      Returns
      -------
      object
         Returns cloned contents of queue buffer.
      """
      
      self._lock_queue.acquire()
      
      contents = []
      
      try:
         if (self._queue_type == flags.QUEUE_TYPE_NONE):
            contents = []
         else:
            contents = self._queue.copy()
      except:
         contents = []
      finally:
         self._lock_queue.release()
      
      return contents
   
   def flow_in (
      self,
      data,
   ):
      """Push data into queue buffer.
      
      Enqueues data, in order, into queue buffer until capacity is not
      exhausted.
      
      Parameters
      ----------
      data : tuple, list, bytearray, object
         Data (list-like) to be pushed into queue buffer.
      
      Returns
      -------
      int
         Returns length of data pushed.
      NoneType
         Returns None if no data supplied.
      """
      
      if (not data):
         return None
      
      self._lock_queue.acquire()
      
      try:
         data_length = 0
         
         for idata in data:
            if (
                  (self._capacity   == -1)
               or (len(self._queue) <  self._capacity)
            ):
               self._queue.append(idata)
               
               data_length += 1
            else:
               break
      finally:
         self._lock_queue.release()
      
      return data_length
   
   def flow_out (
      self,
      data_length=1,
   ):
      """Retrieve data from queue buffer.
      
      Dequeues data, in order, from queue buffer until specified data length
      or till last item in queue.
      
      Parameters
      ----------
      data_length : int
         Length (or number) of data (items) to be retrieved from queue buffer.
      
      Returns
      -------
      object
         Returns list-like sequence of data, in-order.
      """
      
      data_length = int(data_length)
      
      if (data_length < 0):
         data_length = -1
      
      if (not data_length):
         return None
      
      self._lock_queue.acquire()
      
      try:
         data = type(self._queue)()
         
         while (
                 data_length
            and (len(self._queue))
         ):
            data_length -= 1
            
            try:
               idata = self._queue.pop(0)
               data.append(idata)
            except:
               data_length = 0
               break
      finally:
         self._lock_queue.release()
      
      return data
