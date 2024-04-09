import nsim
nsim.libsysmodules.manager.override()

import socket
from nsim.libdebug.intersocketmodules import doubleendeddirectconnector as dedc

if __name__ == '__main__':
   print('DEDC Repeat - Dual socket program\n')
   
   socket_1 = socket.socket()
   socket_2 = socket.socket()
   
   print('DEDC: connecting', end='')
   
   dedc_1 = dedc.doubleendeddirectconnector(
      socket_1=socket_1,
      socket_2=socket_2,
   )
   
   print('\rDEDC: connected !\n')
   
   socket_1.bind((0, 20))
   socket_2.bind((0, 50))
   
   message_1 = str(input('[1]:: Message to send: ')).encode()
   message_2 = str(input('[2]:: Message to send: ')).encode()
   
   print('\n[1]:: Message status: sending', end='')
   message_len = socket_1.sendto(message_1, (0, 50))
   print('\r[1]:: Message status: sent [{0}]'.format(message_len))
   
   print('[2]:: Message status: sending', end='')
   message_len = socket_2.sendto(message_2, (0, 20))
   print('\r[2]:: Message status: sent [{0}]'.format(message_len))
   
   print('\nReceiver\'s message status: waiting to receive', end='')
   
   socket_2.settimeout(-1)
   message_recvd_2 = socket_2.recv(1)
   socket_2.settimeout(None)
   
   socket_1.settimeout(-1)
   message_recvd_1 = socket_1.recv(1)
   socket_1.settimeout(None)
   
   print('\rReceiver\'s message status: received          ')
   print('[1]:: Message received:', message_recvd_1[0].decode())
   print('[2]:: Message received:', message_recvd_2[0].decode())
   
   socket_1.close()
   socket_2.close()
   
   print('\nDual Socket program: completed\n')
   
   exit(0)
