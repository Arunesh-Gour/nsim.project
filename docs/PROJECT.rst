#######
PROJECT
#######

NSIM - Docs: Project
********************
Network Simulator (NSIM), is a concept prototype towards network algorithm
development. It is designed to allow developers to quickly design and test
their (network) algorithms for potentially any layer of the network stack.
This is acheived through a custom ``basesocket`` interface similar to linux
network stack's ``socket`` interface.

What exactly is NSIM ?
======================
NSIM is a prototype of a concept idea for a platform to allow development and
testing of network algorithms (in their concept or proposal stage) on a single
platform without needing any other tools or resources.

Why we need NSIM ?
==================
To better understand this, read the following scenario and the questions that
follow.

Scenario
--------
There are some developers hailing from networking domain. They wish to develop
alternative algorithms for TCP, UDP, IP, etc. For this, they have on paper,
laid down how their custom algorithm, let's say custom UDP algorithm, should
work, specifically about:

*  Packet format.

*  How it would be initialized.

*  How it will send first byte(s) to receiver, for transmitting data.

*  How the receiver will react to first byte(s), for receiving the data.

*  And probably on how it will work with other layers in the network.

Based on this design, they developed a basic prototype (program) without any system calls (or kernel calls) as a demonstration, which can only handle byte data
deliberately fed into the algorithm.

Questions
---------
*  Are there any existing tools or methods that can help them to test their
   algorithm ?

*  If so, what is the easiest way of testing this without changing much of the
   code base ?

*  Can the proposed method allow integrating real application(s) to be tested
   with custom algorithm ?

The answer to the above questions is that there is no simple way of acheiving
this. To do this, they need to use multiple tools and methods, which is
sometimes demotivating for developers, and especially students (or beginners),
due to the time and expertise required.

And so, to solve this situation, this project was conceptualized.

Purpose
=======
The main aims of the project are:

*  Provide single platform for network algorithm development and testing.

*  The platform (project) should be easy to use.

*  Project should closely represent actual design of network stack as in
   real systems.

*  Should be usable by developers, beginners, students and faculties. That is,
   it is more of an educational project.

Why Python ?
============
Python (version 3.8+) provides a lot of advantages over other languages,
specifically (but not limiting to):

*  Widely used.

*  Amount of documentation, resources and help (from co-users) available.

*  Huge library.

*  Simple and easy to understand.

*  Easy to modify.

*  Ability to be used in multiple ways (modes):
   
   *  Interpreted (via interpreter).
   
   *  Interpreted (via scripts).
   
   *  Ability to compile scripts and modules (using other libraries).

And more.

And these advantages directly or in-directly influence the design of NSIM.

Design and Usage
================
Please refer to the presentation (`presentation.nsim.pdf <https://github.com/Arunesh-Gour/nsim.project/blob/main/docs/presentation.nsim.pdf>`_) for the design
and its usage.

Additionally, one can use help documentation by running the `nsim library <
https://github.com/Arunesh-Gour/nsim.project/blob/main/src/nsim/>`_ with the
help flag as: ``python nsim -h``.

Directory structure
-------------------
Directory structure (of main modules) and their short description::
   
   ./nsim/
   |
   |--- libcommon             # common utils
   |--- libdebug              # centralized debugger and tools
   |--- libdriver             # interface drivers - wireless, slip, etc
   |--- libhardwareinterface  # nic, wire, queue buffers, etc
   |--- libnet                # ipv4 - tcp / udp, basesocket, etc
   |--- libprogress           # trigger system
   |___ libsysmodules         # system module override

Built with
==========
*  Python >= 3.8

*  `Brython <https://brython.info/>`_ >= 3.10.5

*  Flask >= 2.3.2

*  `Brython SPA framework <https://github.com/CXINFINITE/ProjectEssentials-Python/blob/main/src/brythonSPA/>`_.

*  `UAPI <https://github.com/CXINFINITE/ProjectEssentials-Python/blob/main/src/UAPI/>`_.

*  `generic-flask-web-app <https://github.com/CXINFINITE/ProjectEssentials-Python/blob/main/src/webapp/flaskwebapps/genericflaskwebapp/>`_.

*  `libcommon <https://github.com/CXINFINITE/ProjectEssentials-Python/blob/main/src/libcommon/>`_.

*  `libprogress <https://github.com/CXINFINITE/ProjectEssentials-Python/blob/main/src/libprogress/>`_.

Tested on
=========
*  ``Ubuntu 22.04``.

Tested with
===========
*  ``Python 3.10.12``.

*  ``Flask 2.3.2``.

*  ``Brython 3.10.5``.

Project's Current State
=======================
This project was started almost a year ago (from now), but is still not
completed (even the concept / prototype version) due to the time constraints.
This can be inferred from the fact that since the inception, somewhat less than
50 hours (around 2 days) (only) are spent on the project.

This project is a prototype of the concept, which itself is not fully
developed.

Project's Future
================
As mentioned, due to time constraints, this project is not in active
development and hence can be considered 'dead'. Though if the conditions
become favourable, then the project can be re-activated, but with a separate
name and repository, which will be mentioned here as well.
