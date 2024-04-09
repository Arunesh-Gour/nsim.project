from nsim.libnet import basesocket
from nsim.libdebug import debugger

from .uapiManager import UAPIManager
from .apiUtilities import APIUtilities
from .apiDecorators import APIDecorators

from threading import (
   Lock,
)

import genericflaskwebapp as app

class Debugger:
   default_index  = 0
   debugger       = debugger.debugger(
      None,
   )
   
   _lock_debugger = Lock()
   
   class Configure:
      def socket_state_current (
         request = None,
         data    = None,
         index   = 0,
      ):
         index = index or data.get('index', 0) or 0
         
         try:
            index = int(str(index).strip().lower())
         except:
            index = 0
         
         index = (
            0
            if (index < 1)
            else (
               len(basesocket.basesocket.basesocket_objects)
               if (index >= len(basesocket.basesocket.basesocket_objects))
               else
               int(index)
            )
         )
         
         data = {
            'default_index' : (
               app.backend.functionality.uapi.debugger.default_index
            ),
         }
         
         if (index):
            data['sockets'] = [
               Debugger.Configure._socket_state_current(
                  index=index,
               ),
            ]
         else:
            data['sockets'] = [
               Debugger.Configure._socket_state_current(
                  index=(index + 1),
               )
               for index in range(
                  len(basesocket.basesocket.basesocket_objects)
               )
            ]
         
         return UAPIManager.createResponse(
            status = True,
            data   = data,
         )
      
      def _socket_state_current (
         index,
      ):
         Debugger._lock_debugger.acquire()
         
         try:
            try:
               basesocket_object = basesocket.basesocket.basesocket_objects[
                  (index - 1)
               ]
            except:
               basesocket_object = None
            
            if (basesocket_object):
               Debugger.debugger.basesocket = basesocket_object
               
               data = {
                  'index'  : index,
                  'status' : basesocket_object._status,
                  'state'  : (
                     Debugger.debugger.progress_mechanism(
                        get_object=True,
                     ).state(
                        describe=False,
                     )
                  ),
                  'mode'   : (
                     Debugger.debugger.progress_mechanism(
                        get_object=True,
                     ).mode(
                        describe=True,
                     )
                  ),
                  'layers' : Debugger.debugger.layers(),
               }
            else:
               data = dict()
            
            return data
         finally:
            Debugger._lock_debugger.release()
         
         return None
      
      def socket_state_alter (
         request  = None,
         data     = None,
         index    = 0,
         activate = None,
      ):
         index    = index or data.get('index', 0) or 0
         activate = (
            activate
            if (activate is not None)
            else
            data.get('activate')
         )
         activate = (
            None
            if (activate is None)
            else (
               False
               if (not activate)
               else (
                  True
                  if (activate)
                  else
                  None
               )
            )
         )
         
         try:
            index = int(str(index).strip().lower())
         except:
            index = 0
         
         index = (
            0
            if (index < 1)
            else (
               len(basesocket.basesocket.basesocket_objects)
               if (index >= len(basesocket.basesocket.basesocket_objects))
               else
               int(index)
            )
         )
         
         if (
                (index)
            and (activate is None)
         ):
            data = {
               'status' : False,
            }
         else:
            data = {
               'status' : True,
            }
            
            if (index):
               data['sockets'] = [
                  Debugger.Configure._socket_state_alter(
                     index    = index,
                     activate = activate,
                  ),
               ]
            else:
               data['sockets'] = [
                  Debugger.Configure._socket_state_alter(
                     index    = (socket_index + 1),
                     activate = activate,
                  )
                  for socket_index in range(
                     len(basesocket.basesocket.basesocket_objects)
                  )
               ]
         
         return UAPIManager.createResponse(
            status = True,
            data   = data,
         )
      
      def _socket_state_alter (
         index,
         activate = None,
      ):
         Debugger._lock_debugger.acquire()
         
         try:
            try:
               basesocket_object = basesocket.basesocket.basesocket_objects[
                  (index - 1)
               ]
            except:
               basesocket_object = None
            
            if (basesocket_object):
               Debugger.debugger.basesocket = basesocket_object
               
               if (activate is None):
                  if (Debugger.debugger.progress_mechanism(
                        get_object=True,
                     ).state(
                        describe=False,
                     )
                  ):
                     activate = False
                  else:
                     activate = True
               
               Debugger.debugger.progress_mechanism(
                  activate = activate,
               )
               
               return True
            
            return False
         finally:
            Debugger._lock_debugger.release()
         
         return None
   
   class Visualize:
      def queue_state_current (
         request = None,
         data    = None,
         index   = 0,
      ):
         index = index or data.get('index', 0) or 0
         
         try:
            index = int(str(index).strip().lower())
         except:
            index = 0
         
         index = (
            0
            if (index < 1)
            else (
               len(basesocket.basesocket.basesocket_objects)
               if (index >= len(basesocket.basesocket.basesocket_objects))
               else
               int(index)
            )
         )
         
         '''
         if (index):
            data = {
               'status' : True,
               'queues' : Debugger.Visualize._queue_state_current(
                  index=index,
               ),
            }
         else:
            data = {
               'status' : False,
            }
         
         return UAPIManager.createResponse(
            status = True,
            data   = data,
         )
         '''
         
         data = {
            'default_index' : (
               app.backend.functionality.uapi.debugger.default_index
            ),
         }
         
         if (index):
            data['sockets'] = [
               Debugger.Visualize._queue_state_current(
                  index=index,
               ),
            ]
         else:
            data['sockets'] = [
               Debugger.Visualize._queue_state_current(
                  index=(index + 1),
               )
               for index in range(
                  len(basesocket.basesocket.basesocket_objects)
               )
            ]
         
         return UAPIManager.createResponse(
            status = True,
            data   = data,
         )
      
      def _queue_state_current (
         index,
      ):
         Debugger._lock_debugger.acquire()
         
         try:
            try:
               basesocket_object = basesocket.basesocket.basesocket_objects[
                  (index - 1)
               ]
            except:
               basesocket_object = None
            
            if (basesocket_object):
               Debugger.debugger.basesocket = basesocket_object
               
               data = {
                  'index'  : index,
                  'status' : basesocket_object._status,
                  'state'  : (
                     Debugger.debugger.progress_mechanism(
                        get_object=True,
                     ).state(
                        describe=False,
                     )
                  ),
                  'mode'   : (
                     Debugger.debugger.progress_mechanism(
                        get_object=True,
                     ).mode(
                        describe=True,
                     )
                  ),
                  'queues' : Debugger.debugger.queues(state=True),
               }
            else:
               data = dict()
            
            return data
         finally:
            Debugger._lock_debugger.release()
         
         return None
   
   def _visualize (
      index,
   ):
      # Debugger.default_index = index
      app.backend.functionality.uapi.debugger.default_index = index
      
      return True
