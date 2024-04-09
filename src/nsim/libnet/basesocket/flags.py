class Flags:
   """Flags for BaseSocket object.
   """
   
   SOCK_FAMILY_NONE     = 1
   AF_INET              = 2
   AF_INET6             = 4
   
   SOCK_TYPE_NONE       = 1
   SOCK_STREAM          = 2
   SOCK_DGRAM           = 4
   
   SOCK_PROTO_NONE      = 1
   
   SHUT_NONE            = 1
   SHUT_RD              = 2
   SHUT_WR              = 4
   SHUT_RDWR            = 6
   
   STATUS_NONE          = 1
   STATUS_OPEN          = 2
   STATUS_BOUND         = 4
   STATUS_CONNECTED     = 8
