from .uapiManager import UAPIManager
from .apiUtilities import APIUtilities
from .apiDecorators import APIDecorators

from .debugger import Debugger

class APIs:
   loaded = None
   apis = dict()
   
   def start ():
      if (APIs.loaded):
         return None
      
      APIs.apis = {
         'api.getcodes': (APIs.api_getcodes, 0,),
         'api.test': (APIs.api_test, 10),
         
         'socket.state.current' : (
            Debugger.Configure.socket_state_current, 1,
         ),
         'socket.state.alter' : (
            Debugger.Configure.socket_state_alter, 2,
         ),
         
         'queue.state.current' : (
            Debugger.Visualize.queue_state_current, 1,
         ),
      }
      
      for apicode, api_details in APIs.apis.items():
         UAPIManager.registerAPI(apicode, *api_details)
      
      APIs.loaded = True
   
   def api_test (request=None, data=None, *args,):
      return UAPIManager.createResponse(
         status=True, reason=UAPIManager.Status.Reason.LOGIN_REQUIRED,
         responseData='Well done! I\'m good!', yourData=data,
         args=args,
      )
   
   def api_getcodes (request=None, data=None):
      return UAPIManager.createResponse(
         status=True, apicodes=list(UAPIManager.getAvailableAPIs()),
      )
