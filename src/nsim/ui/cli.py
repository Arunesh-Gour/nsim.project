import os
import argparse
import nsim as app

def argparser_get ():
   parser = argparse.ArgumentParser(
      formatter_class=argparse.RawDescriptionHelpFormatter,
      description=(
         '{0}:\n'.format(
            app.__version__.appname,
         )
         + '''
      NSIM Library
      ============
      NSIM, a concept prototype, is a package of simple, yet powerful tools and
      libraries allowing developers to develop and debug custom network
      algorithms with ease and efficiency.
      But being a concept prototype, its functionality and practicality is
      vastly limited.
      
      Working with
      ============
      This project is meant to be used as a library, as illustrated below with
      some examples.
      
      Algorithm development
      ---------------------
      If you want to load custom algorithms to nsim and work with them, simply
      head over to 'nsim/libnet/basesocket/_basesocket.py' file.
      There, append your algorithm(s) in 'basesocket()' function at appropriate
      place. Make sure your algorithms are import-able in this file or at-least
      in the function.
      
      Following functions should be defined in your algorithm:
      *  process (self):
         Simple function to progress or advance your algorithm's task by one
         step.
      *  stream (
            stream_up_in     = None, # link: down -> up; upper layer
            stream_up_out    = None, # link: up -> down; upper layer
            stream_down_in   = None, # link: up -> down; lower layer
            stream_down_out  = None, # link: down -> up; lower layer
         ):
         Function to allow setting steams (queue buffers) for debugging and
         data transfer between layers.
         Also, you should define the type of queues your algorithm expects, in
         '_basesocket.py' file, while working so that BaseSocket can set them
         up wrt other layers in consideration.
         Usually queue buffers are expected to be of type list or bytearray.
      *  ip (ip_source, ip_destination)
         Optional, function to set source and destination ip if required.
      *  port (port_source, port_destination)
         Optional, function to set source and destination ports if required.
      
      Development
      -----------
      In your python program, use nsim's libnet.basesocket module instead of
      built-in socket module, with almost similar interface.
      Alternatively, if you want to use it over existing programs without
      needing to change much in your project, use nsim.libsysmodules to
      override system socket module with basesocket module without need to
      change anything else.
      
      Example 1, un-overridden mode::
         
         from nsim.libnet import basesocket
         
         socket_1 = basesocket.basesocket(
            basesocket.flags.AF_INET,
            basesocket.flags.SOCK_DGRAM,
         )
         
         socket_1.bind(
            (
               0,    # ip (int, for now)
               5001, # port
            ),
         )
         
         socket_1.sendto(
            b'Namaste !', # message
            (             # receiver's address
               20,    # ip (int, for now)
               5008, # port
            ),
         )
         
         # Un-comment to recv:
         # print(
         #    'Received message:',
         #    socket_1.recv(
         #       1, # maximum number of messages
         #    ),
         # )
         
         socket_1.close()
      
      Example 2, for normal (overridden) mode::
         
         import nsim
         # nsim's import automatically overrides system modules by default.
         import socket
         
         socket_1 = socket.socket(
            socket.AF_INET,
            socket.SOCK_DGRAM,
         )
         
         socket_1.bind(
            (
               0,    # ip (int, for now)
               5001, # port
            ),
         )
         
         socket_1.sendto(
            b'Namaste !', # message
            (             # receiver's address
               20,    # ip (int, for now)
               5008, # port
            ),
         )
         
         # Un-comment to recv:
         # print(
         #    'Received message:',
         #    socket_1.recv(
         #       1, # maximum number of messages
         #    ),
         # )
         
         socket_1.close()
      
      Example 3, working with libsysmodules::
         
         from nsim import libsysmodules
         
         # Manual overriding :
         libsysmodules.manager.override()
         
         # socket is basesocket
         import socket
         del socket
         
         # Get original, built-in socket module irrespective of override.
         socket = libsysmodules.manager.module_original('socket')
         del socket
         
         # Manual restoration :
         libsysmodules.manager.restore()
         
         # socket is original, built-in socket module
         import socket
         del socket
         
         # Check if modules are overridden :
         libsysmodules.manager.is_overridden() # return True or False
         # Currently returns False.
         
         # libsysmodules affects entire program, not just one file.
         # So, use carefully.
      
      Debugging
      ---------
      With nsim, there are multiple ways to debug your basesocket object.
      Generally, the debuggers are meant to be used over existing basesocket
      objects. Make sure to set up at-least one before proceeding.
      
      Example 1, using libdebug.debugger::
         
         # Assuming socket_1 is a pre-initialized basesocket object.
         # socket_1
         
         from nsim.libdebug import debugger
         debugger_1 = debugger.debugger(socket_1)
         
         print(
            'Progress mechanism library used with socket_1:',
            debugger_1.progress_mechanism,
         )
         # Progress mechanism library used with socket_1: trigger
         
         # Deactivate progress mechansim bound to socket_1 :
         debugger_1.progress_mechansim(activate=False)
         
         socket_1.sendto(b'Namaste!', (20, 5008))
         
         print(
            'Layers (with index):',
            debugger_1.layers(),
         )
         # Lists names of all layers attached to socket_1 as:
         # Layers (with index):
         # [
         #    [1, 'application'],
         #    [2, 'simplifiedudp'],
         #    [3, 'ipv4'],
         #    [4, 'simplifiedslip'],
         #    [5, 'physical'],
         # ]
         
         print(
            'Queues (with contents):',
            debugger_1.queues(contents=True),
         )
         # Lists queues with their current content in their buffers:
         # Queues (with contents):
         # [
         #    [[b'Namaste!',], []],
         #    [[], []],
         #    [[], []],
         #    [[], []],
         # ]
         
         # Activate progress mechansim bound to socket_1 :
         debugger_1.progress_mechansim(activate=True)
      
      Example 2, using libdebug.gfxdebuggers.webvisualizerdebugger::
         
         # Assuming socket_1 is a pre-initialized basesocket object.
         # socket_1
         
         from nsim.libdebug.gfxdebuggers import webvisualizerdebugger
         
         wvd_manager = webvisualizerdebugger.manager(
            ip   = '0.0.0.0',
            port = 5001,
         )
         
         # focus on socket_1 during visualization
         wvd_manager.visualize(socket_1)
         
         # Start web server in blocking mode.
         wvd_manager.start()
         
         # Head over to web browser and type:
         # http://127.0.0.1:5001/
         # This should take you to web visualizer debugger's web page.
         # Select debug tab and visualize and debug you sockets.
         
         # Press [Ctrl-C] to terminate.
      
      Getting help
      ------------
      For help related to modules, use in-built help function to go through
      provided docstrings.
      
      Example 1, fetching docstrings::
         
         # open python interpreter for better experience:
         
         import nsim
         from nsim.libnet import basesocket
         
         # For help on packages:
         help(nsim)
         help(nsim.libnet)
         
         # For help with classes and their functions:
         help(basesocket)
         help(basesocket.close)
         
         exit(0)
      
      Additional help
      ---------------
      For additional help or information like documentation, usage and other
      resources, please refer to the project's github page.
      
      Github: https://github.com/Arunesh-Gour/nsim.project/
      
         '''
      ),
      epilog=(
         (
              '< Designer & Developer />\n'
            + '[| {0} |]\n'
            + 'Github : {1}\n'
            + 'Project: {2}\n'
         ).format(
            app.__author__.name,
            app.__author__.github,
            'https://github.com/Arunesh-Gour/nsim.project/',
         )
      ),
   )
   
   parser.add_argument(
      '-V', '--version',
      action='version',
      version=('{0}'.format(
            app.__version__.description,
         )
      ),
   )
   
   return parser

def argparser_parse_args (*args, **kwargs):
   parser = argparser_get()
   parsed = parser.parse_args(*args, **kwargs)
   
   return (parser, parsed)

def execute ():
   parser, parsed_args = argparser_parse_args()
   
   if (not parsed_args):
      raise Exception('ui.cli.execute: cli not parsed')
   
   return parsed_args
