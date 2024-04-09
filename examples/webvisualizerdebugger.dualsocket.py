import nsim
nsim.libsysmodules.manager.override()

import socket
from nsim.libdebug import debugger
from nsim.libdebug.gfxdebuggers import webvisualizerdebugger
from nsim.libdebug.intersocketmodules import doubleendeddirectconnector as dedc

import time
from threading import (
   Event,
   Thread,
)

if __name__ == '__main__':
   print('Web Visualizer Debugger - Dual socket program\n')
   
   socket_1 = socket.socket()
   socket_2 = socket.socket()
   
   dedc_1 = dedc.doubleendeddirectconnector(
      socket_1=socket_1,
      socket_2=socket_2,
   )
   
   socket_1.bind((0, 20))
   socket_2.bind((0, 50))
   
   webvisualizerdebugger_1 = webvisualizerdebugger.manager(
      ip   = '127.0.0.1',
      port = 5000,
   )
   debugger_1 = debugger.debugger(socket_1)
   debugger_2 = debugger.debugger(socket_2)
   
   debugger_1.progress_mechanism(activate=False)
   debugger_2.progress_mechanism(activate=False)
   
   event_threads_active = Event()
   event_threads_active.set()
   
   def toggle_progress_mechanism (
      webvisualizerdebugger_1 = webvisualizerdebugger_1,
      event_threads_active    = event_threads_active,
      
      debugger_1 = debugger_1,
      debugger_2 = debugger_2,
   ):
      time.sleep(1)
      
      while (event_threads_active.wait(0.0)):
         debugger_1.progress_mechanism(
            activate = bool(not (debugger_1.progress_mechanism(
               get_object=True
            ).state(describe=False))),
         )
         debugger_2.progress_mechanism(
            activate = bool(not (debugger_1.progress_mechanism(
               get_object=True
            ).state(describe=False))),
         )
         
         time.sleep(4)
      
      return None
   
   def toggle_socket_visualization (
      webvisualizerdebugger_1 = webvisualizerdebugger_1,
      event_threads_active    = event_threads_active,
      
      socket_1 = socket_1,
      socket_2 = socket_2,
   ):
      time.sleep(1)
      
      visualized_primary = True
      
      while (event_threads_active.wait(0.0)):
         webvisualizerdebugger_1.visualize(
            socket = (
               socket_1
               if (not visualized_primary)
               else
               socket_2
            ),
         )
         visualized_primary = bool(not visualized_primary)
         
         time.sleep(6)
      
      return None
   
   def messages_send (
      webvisualizerdebugger_1 = webvisualizerdebugger_1,
      event_threads_active    = event_threads_active,
      
      socket_1 = socket_1,
      socket_2 = socket_2,
   ):
      time.sleep(1)
      
      while (event_threads_active.wait(0.0)):
         socket_1.sendto(b'Namaste 2!', (0, 50))
         socket_2.sendto(b'Namaste 1!', (0, 20))
         
         time.sleep(1)
      
      return None
   
   def messages_recv (
      webvisualizerdebugger_1 = webvisualizerdebugger_1,
      event_threads_active    = event_threads_active,
      
      socket_1 = socket_1,
      socket_2 = socket_2,
   ):
      time.sleep(1)
      
      while (event_threads_active.wait(0.0)):
         socket_1.settimeout(1)
         socket_1.recv(10)
         
         socket_2.settimeout(1)
         socket_2.recv(10)
         
         time.sleep(1)
      
      return None
   
   def queue_state_print (
      webvisualizerdebugger_1 = webvisualizerdebugger_1,
      event_threads_active    = event_threads_active,
      
      debugger_1 = debugger_1,
      debugger_2 = debugger_2,
   ):
      time.sleep(1)
      
      while (event_threads_active.wait(0.0)):
         print('[1] State:', debugger_1.queues(state=True))
         print('[2] State:', debugger_2.queues(state=True))
         
         # print('[1] Contents:', debugger_1.queues(contents=True))
         # print('[2] Contents:', debugger_2.queues(contents=True))
         
         time.sleep(4)
      
      return None
   
   print('Utility threads: Starting', end='')
   
   Thread(
      target=toggle_progress_mechanism,
      daemon=True,
   ).start()
   Thread(
      target=toggle_socket_visualization,
      daemon=True,
   ).start()
   Thread(
      target=messages_send,
      daemon=True,
   ).start()
   Thread(
      target=messages_recv,
      daemon=True,
   ).start()
   Thread(
      target=queue_state_print,
      daemon=True,
   ).start()
   
   print('\rUtility threads: Started ')
   
   print('Web Visualizer Debugger: Started !')
   
   try:
      webvisualizerdebugger_1.state(activate=True)
      time.sleep(0.2)
      webvisualizerdebugger_1.start()
   except:
      pass
   finally:
      event_threads_active.clear()
      
      print('Web Visualizer Debugger: Terminated !')
      
      socket_1.close()
      socket_2.close()
   
   print('\nDual Socket program: completed\n')
   
   exit(0)
