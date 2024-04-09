from .flags import Flags as flags
from .descriptors import Descriptors as descriptors
from ._basesocket import _BaseSocket

# import nsim as app

from nsim.libprogress import trigger

class BaseSocket (_BaseSocket):
   """BaseSocket object for development and debugging of network algorithms.
   
   Development and debug oriented replacement for built-in socket library,
   meant to be used with nsim's library for developing and debugging network
   algorithms.
   This is the core of nsim project. It mimics built-in socket library to some
   extent, just enough to support algorithm development.
   This is a child class inheriting the core _BaseSocket class.
   This class adds progress mechanism over core _BaseSocket class for automated
   and synchronous progression for easy debugging.
   To add your own algorithms to this, modify the file for base class and
   include one.
   
   Attributes
   ----------
   basesocket_objects : list
      List of currently active basesocket objects, to be used by debugger.
   ProgressionSystem : class
      Class defining currently used progression system with custom api to it.
   _progress_mechanism : object
      Progress mechanism object attached to basesocket.
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
   _timeout : int
      Timeout value, to be used by various operations.
   _status : int
      Status flag for socket's current state.
   
   Methods
   -------
   __init__ (sock_family, sock_type, sock_proto)
      Init basesocket with specified configurations and progress mechanism.
   basesocket ()
      Configures layers and queues for basesocket.
   bind ()
      Binds basesocket to address.
   connect ()
      Connects basesocket to destination address.
   disconnect ()
      Disconnects basesocket from destination.
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
   
   # BaseSocket object
   # BaseSocket external public lib / functions (callable as fun(socket))
   
   basesocket_objects = list()
   
   class ProgressionSystem:
      """Static class for defining progress mechanism with custom apis.
      
      This provides static configuration and apis to currently used progress
      mechanism, removing the need for the user to manually configure these.
      The methods and attributes defined here are used by BaseSocket's wrapper
      class to initialize progress mechanisms for each object.
      
      Attributes
      ----------
      library_name : str
         Name of library used for progress mechanism.
      library : object
         Library object (or module) for progress mechanism.
      flags : class
         Flags class for progress mechanism.
      descriptors : class
         Descriptors class for progress mechanism.
      init_function : callable
         Callable init method to initialize progress mechanism.
      init_args : list
         Default configuration for progress mechanism as args.
      init_kwargs : dict
         Default configuration for progress mechanism as kwargs.
      
      Methods
      -------
      pre_init ()
         Performs pre-init configurations on basesocket object.
      post_init ()
         Performs post-init configurations on basesocket object.
      bind ()
         Custom api to bind any function to basesocket's progress mechanism.
      notification_alert ()
         Custom api to register for progress mechanism's notifications.
      """
      
      library_name  = 'trigger'
      library       = trigger
      flags         = trigger.flags
      descriptors   = trigger.descriptors
      
      init_function = trigger.trigger
      
      init_args     = []
      init_kwargs   = {
         'mode'                            : trigger.flags.MODE_HYBRID,
         
         'interval_trigger_activation'     : 0.1,
         'interval_trigger'                : 0.2,
         'interval_min'                    : 0.3,
         'interval_max'                    : 0.4,
         'interval_critical'               : 0.5,
         'interval_trigger_auto_add'       : 1.0,
         
         'retries_trigger_auto_add'        : 3,
         
         'clock_interval'                  : 0.1,
         'clock_step'                      : 0.1,
         
         'interval_exceed_action_min'      : (
            trigger.flags.INTERVAL_EXCEED_ACTION_IGNORE
         ),
         'interval_exceed_action_max'      : (
            trigger.flags.INTERVAL_EXCEED_ACTION_TRIGGER_FORCE
         ),
         'interval_exceed_action_critical' : (
            trigger.flags.INTERVAL_EXCEED_ACTION_NOTIFY
         ),
         
         'debug_log'                      : False,
         'debug_trace'                    : True,
      }
      
      def pre_init (basesocket):
         """Performs pre-init configurations on basesocket object.
         
         Performs pre-init configurations on basesocket object based on
         currently used progress mechanism.
         Meant to be called before initializing progress mechanism on
         basesocket object.
         Currently, does nothing.
         
         Parameters
         ----------
         basesocket : BaseSocket
            BaseSocket object on which pre-init configuration are to run.
         
         Returns
         -------
         NoneType
            Returns None.
         """
         
         return None
      
      def post_init (basesocket):
         """Performs post-init configurations on basesocket object.
         
         Performs post-init configurations on basesocket object based on
         currently used progress mechanism.
         Meant to be called after initializing progress mechanism on
         basesocket object.
         Currently, binds all layers' process methods, attached to basesocket,
         to progress mechanism to automatically and centrally synchronize
         their progression.
         Also, sets up progress mechanism's operation mode, but keeps it
         disabled for later use.
         
         Parameters
         ----------
         basesocket : BaseSocket
            BaseSocket object on which post-init configuration are to run.
         
         Returns
         -------
         NoneType
            Returns None.
         """
         
         # Appending in reverse for better debug experience with debugger.
         for index in range((len(basesocket._layers) - 1), -1, -1):
            basesocket._progress_mechanism.trigger_bind(
               trigger_bound_function = basesocket._layers[index].process,
               times_retain           = -1,
               times_recurse          = -1,
               non_blocking           = True,
               thread_daemon          = True,
            )
         
         basesocket._progress_mechanism.mode(
            mode=BaseSocket.ProgressionSystem.init_kwargs['mode'],
            activate=False,
            non_blocking=True,
         )
         
         return None
      
      def bind (
         basesocket,
         
         bind_function,
          *args,
         **kwargs,
      ):
         """Custom api to bind any function to basesocket's progress mechanism.
         
         Binds bind_function to basesocket's progress mechanism as per apis
         of progress mechanism. This eliminates user's need to check for apis
         pertaining to the progress mechanism specifically.
         
         Parameters
         ----------
         basesocket : BaseSocket
            BaseSocket object whose progress mechanism is to be used to bind.
         bind_function : callable
            Function to be bound to progress mechanism for automated execution.
         args : list
            Additional arguments to progress mechanism's bind method.
         kwargs : dict
            Additional keyed-arguments to progress mechanism's bind method.
         
         Returns
         -------
         bool
            Returns True or alive status for executor thread for bind.
         """
         
         return (basesocket._progress_mechanism.trigger_bind(
            *args,
            trigger_bound_function = bind_function,
            **kwargs,
         ))
      
      def notification_alert (
         basesocket,
         
         *args,
         
         callback = None,
         events   = None,
         
         **kwargs,
      ):
         """Custom api to register for progress mechanism's notifications.
         
         Registers (or binds) callback with basesocket's progress mechanism
         as per its apis. This eliminates user's need to check for apis
         pertaining to the progress mechanism specifically.
         Not specifying events automatically picks default set of events.
         
         Parameters
         ----------
         basesocket : BaseSocket
            BaseSocket object whose progress mechanism is to be used to bind.
         callback : callable, NoneType, default=None
            Callback, used upon alert generation.
         events : int, NoneType, default=None
            Events upon which notification alert is to be sent, None for auto.
         args : list
            Additional arguments to progress mechanism's notifier method.
         kwargs : dict
            Additional keyed-arguments to progress mechanism's notifier method.
         
         Returns
         -------
         str
            Returns identifier used to register for notifications.
         bool
            Returns success for unregistration or failed registration.
         """
         
         if (events is None):
            events = (
                 trigger.flags.INTERVAL_EVENT_TRIGGER
               | trigger.flags.INTERVAL_EVENT_TRIGGER_PRE_MIN_FORCE
               | trigger.flags.INTERVAL_EVENT_TRIGGER_FORCE
            )
         
         return basesocket._progress_mechanism.notification_alert(
            *args,
            callback = callback,
            events   = events,
            **kwargs,
         )
   
   def __init__ (
      self,
      *args,
      **kwargs,
   ):
      """Init basesocket with specified configurations and progress mechanism.
      
      Wraps base class's init method and additionally attaches progress
      mechanism to the basesocket object.
      
      Parameters
      ----------
      sock_family : int, default=flags.AF_INET
         Socket address family.
      sock_type : int, default=flags.SOCK_DGRAM
         Socket type.
      sock_proto : int, default=flags.SOCK_PROTO_NONE
         Socket protocol number.
      """
      
      self._progress_mechanism = None
      
      super().__init__(*args, **kwargs)
      
      BaseSocket.ProgressionSystem.pre_init(self)
      self._progress_mechanism = BaseSocket.ProgressionSystem.init_function(
          *BaseSocket.ProgressionSystem.init_args,
         **BaseSocket.ProgressionSystem.init_kwargs,
      )
      BaseSocket.ProgressionSystem.post_init(
         self,
      )
      
      if (self not in BaseSocket.basesocket_objects):
         BaseSocket.basesocket_objects.append(self)
