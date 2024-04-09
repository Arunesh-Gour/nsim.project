import WebApplication as App

class DataManager:
   default_index = 0
   state_sockets = dict()
   
   index_sockets_visible = list()
   
   dataRetrieveErrorMessage = (
      'Error retrieving sockets\' data.'
      + '<BR /><BR />Please check your internet connection.'
   )
   
   class Flags:
      STATUS_NONE          = 1
      STATUS_OPEN          = 2
      STATUS_BOUND         = 4
      STATUS_CONNECTED     = 8
   
   def state_socket_retrieve (
      event = None,
      index = 0,
      queue = False,
   ):
      try:
         index = int(str(index).strip())
      except:
         index = 0
      
      data = App.core.UAPIManager.apiCall(
         '{0}.state.current'.format((
            'queue'
            if (queue)
            else
            'socket'
         )),
         data=App.core.UAPIManager.createData(
            index=index,
         ),
         blocking=True,
      )
      
      if (data.get('status') != App.Configuration.STATUS_SUCCESS):
         if (data.get('status') == App.Configuration.STATUS_CONNECTION_ERROR):
            return None
         else:
            return False
      
      data = data.get('data')
      
      DataManager.default_index = data.get(
         'default_index',
      ) or DataManager.default_index or 0
      
      for state_socket in (data.get('sockets') or []):
         if (not DataManager.state_sockets.get(
            state_socket.get('index'),
         )):
            DataManager.state_sockets[
               state_socket.get('index')
            ] = dict()
         
         DataManager.state_sockets[
            state_socket.get('index')
         ]['index'] = state_socket.get('index')
         DataManager.state_sockets[
            state_socket.get('index')
         ]['status'] = state_socket.get('status')
         DataManager.state_sockets[
            state_socket.get('index')
         ]['state'] = state_socket.get('state')
         DataManager.state_sockets[
            state_socket.get('index')
         ]['mode'] = state_socket.get('mode')
         DataManager.state_sockets[
            state_socket.get('index')
         ][(
            'queues'
            if (queue)
            else
            'layers'
         )] = state_socket.get((
            'queues'
            if (queue)
            else
            'layers'
         ))
      
      return True
   
   def state_socket_alter (
      event    = None,
      index    = 0,
      activate = None,
   ):
      try:
         index = int(str(index).strip())
      except:
         index = 0
      
      if (activate is None):
         pass
         # activate = None
      else:
         try:
            activate = bool(activate)
         except:
            activate = None
      
      if (
             (index)
         and (activate is None)
      ):
         return None
      
      data = App.core.UAPIManager.apiCall(
         'socket.state.alter',
         data=App.core.UAPIManager.createData(
            index=index,
            activate=activate,
         ),
         blocking=True,
      )
      
      if (data.get('status') != App.Configuration.STATUS_SUCCESS):
         if (data.get('status') == App.Configuration.STATUS_CONNECTION_ERROR):
            return None
         else:
            return False
      
      data = data.get('data')
      
      return data
   
   def resolve_status_str (event=None, status=0):
      try:
         status = int(status)
      except:
         status = 0
      
      if (status & DataManager.Flags.STATUS_CONNECTED):
         return 'connected'
      elif (status & DataManager.Flags.STATUS_BOUND):
         return 'open & bound'
      elif (status & DataManager.Flags.STATUS_OPEN):
         return 'open'
      elif (status & DataManager.Flags.STATUS_NONE):
         return 'closed'
      else:
         return 'status.unknown'
      
      return None
