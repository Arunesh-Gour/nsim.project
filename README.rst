######
README
######

NSIM
****
Network Simulator (NSIM), is a concept prototype towards network algorithm
development. It is designed to allow developers to quickly design and test
their (network) algorithms for potentially any layer of the network stack.
This is acheived through a custom ``basesocket`` interface similar to linux
network stack's ``socket`` interface.

For detailed information, please refer to `docs/ <https://github.com/Arunesh-Gour/nsim.project/blob/main/docs/>`_ section.

Getting Started
===============
To start developing with nsim, please install requirements from
`requirements.txt <https://github.com/Arunesh-Gour/nsim.project/blob/main/requirements.txt>`_ as:

``pip3 install -r requirements.txt``.

For a graphical introduction, please find the presentation in `docs/ <https://github.com/Arunesh-Gour/nsim.project/blob/main/docs/>`_ section.

Usage
=====
NSIM is designed for both development and testing, which needs to be addressed
in different ways. And so, NSIM offers two separate methods, one for each as
listed in following sections.

Development
-----------
Since the algorithm development requires one to add algorithm(s) to the
``basesocket`` interface, hence NSIM, for now, allows this by directly
modifying internal files.

Steps to add algorithm to NSIM:

*  Make a copy of `src/nsim/ <https://github.com/Arunesh-Gour/nsim.project/blob/main/src/nsim/>`_ and store it in your project directory.

*  In this copy, store your algorithm at an appropriate place, making sure that
   it is import-able by NSIM's ``basesocket`` library (inside ``libnet``).

*  Modify `nsim/libnet/basesocket/_basesocket.py <https://github.com/Arunesh-Gour/nsim.project/blob/main/src/nsim/libnet/basesocket/_basesocket.py>`_ file to
   include your algorithm in ``basesocket()`` method.

*  Add appropriate flags and descriptors for your algorithm in `nsim/libnet/basesocket/flags.py <https://github.com/Arunesh-Gour/nsim.project/blob/main/src/nsim/libnet/basesocket/flags.py>`_ and `nsim/libnet/basesocket/descriptors.py <https://github.com/Arunesh-Gour/nsim.project/blob/main/src/nsim/libnet/basesocket/descriptors.py>`_ files.

*  Save these modifications.

Now, your custom algorithm is ready for testing.

Testing
-------
For testing, NSIM provides an interface similar to python's ``socket``
interface, known as ``basesocket`` interface. Owing to the design of NSIM,
this ``basesocket`` interface can be accessed majorly in two ways (not limited
to) as illustrated in following examples. The examples are made in a way that
they can be either interpreted, used as (in) a script, or in a module depending
on one's needs.

Before proceeding to examples, make sure that ``nsim`` `library <https://github.com/Arunesh-Gour/nsim.project/blob/main/src/nsim/>`_ , the modified one in
case you're developing custom algorithm, is import-able in your scripts.

If not using a modified one, make sure that either ``nsim`` (or a copy of
`src/nsim/ <https://github.com/Arunesh-Gour/nsim.project/blob/main/src/nsim/>`_
) is present in python's path, or make clone of `src/nsim/ <https://github.com/Arunesh-Gour/nsim.project/blob/main/src/nsim/>`_ and store it in your project
directory.

Example 1, for directly using ``basesocket`` interface as is::
   
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
   
   socket_1.close()

Example 2, to use ``basesocket`` interface as python's ``socket`` interface
by overriding it (useful in large projects where modifying individual sections
is difficult)::
   
   import nsim
   
   # nsim's import automatically overrides system modules by default.
   # If not, then manually override as follows :
   # nsim.libsysmodules.manager.override()
   
   # Now, socket refers to basesocket interface only.
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

In the (above) example 2, if, after overriding, you want to revert override or
get original ``socket`` module irrespective of override state (in any case),
see this example (3)::
   
   import nsim
   
   # nsim's import automatically overrides system modules by default.
   # If not, then manually override as follows :
   # nsim.libsysmodules.manager.override()
   
   # Now, socket refers to basesocket interface only.
   import socket
   
   python_socket = nsim.libsysmodules.manager.module_original(
      'socket', # Name of module (to get original)
   )
   
   print (socket == python_socket)
   # Prints False
   
   print(libsysmodules.manager.is_overridden())
   # Prints True
   
   # To restore override:
   nsim.libsysmodules.manager.restore()
   
   print(libsysmodules.manager.is_overridden())
   # Prints False
   
   del socket
   import socket
   
   print (socket == python_socket)
   # Prints True

Refer to `examples/ <https://github.com/Arunesh-Gour/nsim.project/blob/main/examples/>`_ section for more examples.

Release & Version
=================
:Release: Concept Prototype
:Version: 0.1.0

Project's Future
================
NSIM is a concept prototype and hence is provided as is. This project will not
receive any further updates or improvements. Though some bug fixes or general
fix (if deemed necessary) may be released (but not surely).

Though there are chances that a full project (not a concept and / or prototype)
will be developed in near future, if the time and conditions are favourable.

So, for now, it is safe to say that this project is 'dead' !

LICENSE
=======
This project is released under MIT License.

Please refer to `LICENSE <https://github.com/Arunesh-Gour/nsim.project/blob/main/LICENSE>`_ file.
