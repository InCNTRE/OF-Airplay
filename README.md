OF-Airplay
==========

A project to allow secure AirPlay connectivity between devices using OpenFlow.
OF-Airplay is a built with the POX contoller

POX is a network controller written in Python.

POX officially requires Python 2.7 (though much of it will work fine
fine with Python 2.6), and should run under Linux, Mac OS, and Windows.
You can place a pypy distribution alongside pox.py (in a directory
named "pypy"), and POX will run with pypy (this can be a significant
performance boost!).

POX currently communicates with OpenFlow 1.0 switches.

pox.py boots up POX. It takes a list of module names on the command line,
locates the modules, calls their launch() function (if it exists), and
then opens up a Python commandline for interactive use.

To start the Airplay proxy run:

  ./pox.py forwarding.airplay

You can pass options to the modules by specifying options after the module
name.  These are passed to the module's launch() funcion.  For example,
to set the address or port of the controller, invoke as follows:

  ./pox.py forwarding.airplay --address=10.1.1.1 --port=6634

pox.py also supports a few command line options of its own which should
be given first:
 --verbose      print stack traces for initialization exceptions
 --no-cli       don't bring up a Python interpreter
 --no-openflow  don't start the openflow module automatically

