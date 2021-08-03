###########################################
PyTimer, a simple commandline timer utility
###########################################
This is a simple tool that one can call on the CLI to act as either a timer,
with a settable length of time, or a stopwatch.  One simply needs to run the
program with the ``timer`` or ``stopwatch`` options, and choose any options as
needed, and the program will run on the command line until it's stopped with a
CTRL + C or, in the case of the timer, the time runs out.

*****
Timer
*****
To use the timer function, just input the ``timer`` arg to ``timer.py`` and then
use the ``--settime`` arg to set the length of time for the timer.  The length
of the timer can be seconds, hours, or minutes, and can be set with either the
older ``HH:MM:SS`` notation (e.g. 01:05:00 for 1 hour, 5 minutes), or with the
new ``h``, ``m``, ``s`` notation (e.g. ``1h5m``).  Note that with the new
notation method, one does not need to enter all elements of the timer, and can
just enter what they need.  So, for example, if one wanted a 30 second timer,
they would have to enter ``00:00:30`` using the old notation, and ``30s`` using
the new format.  Eventually, the older format may be deprecated in favor of the
new one if it's favored.

*********
Stopwatch
*********
The ``stopwatch`` method will simply start and upward counting timer to help
track the length of time something takes.  This method will run until the user
presses CTRL + c to stop.

**************
Other Features
**************
Any sound can be used for when one is using the ``timer`` function and time has
expired.  There are 3 sound files included for now as choices.  However, one
need only using the ``--tone`` argument and supply it with an MP3 file.  This
feature has not yet been fully tested, and so there may be some system specific
and / or MP3 specific issues with playback.  
