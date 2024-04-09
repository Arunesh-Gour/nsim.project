class Flags:
   """Flags for simplified SLIP (protocol).
   """
   
   SPECIAL_END     = (192).to_bytes(1, 'big')
   SPECIAL_ESC     = (219).to_bytes(1, 'big')
   SPECIAL_ESC_END = (220).to_bytes(1, 'big')
   SPECIAL_ESC_ESC = (221).to_bytes(1, 'big')
