import nsim
nsim.libsysmodules.manager.override()

import socket
from nsim.libdebug.intersocketmodules import doubleendeddirectconnector as dedc

if __name__ == '__main__':
   print('Echo / DEDC Repeat - Single socket program\n')
   
   socket_1 = socket.socket()
   
   print('DEDC: connecting', end='')
   
   dedc_1 = dedc.doubleendeddirectconnector(
      socket_1=socket_1,
      socket_2=socket_1,
   )
   
   print('\rDEDC: connected !\n')
   
   socket_1.bind((0, 20))
   
   message = str(input('Message to send: ')).encode()
   
   print('Message status: sending', end='')
   
   message_len = socket_1.sendto(message, (0, 50))
   
   print('\rMessage status: sent [{0}] '.format(message_len))
   
   print('Receiver\'s message status: waiting to receive', end='')
   
   socket_1.settimeout(-1)
   message_recvd = socket_1.recv(1)
   
   print('\rReceiver\'s message status: received          ')
   print('Message received:', message_recvd[0].decode())
   
   socket_1.settimeout(None)
   
   socket_1.close()
   
   print('\nSingle Socket program: completed\n')
   
   exit(0)
