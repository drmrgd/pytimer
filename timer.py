#!/usr/bin/env python3
# Simple timer program
#
# 1/16/2020 - D Sims
"""
Rudimentary timer program to either count down time with an alarm, or count
elapsed time like a stopwatch.  
"""
import re
import os
import sys
import time
import argparse

from pprint import pprint as pp # noqa

# Need to change an env variable to suppress start up message
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

version = '2.0.080321'

# Globals
mfile = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resource', 
        'me-too.mp3')
if not os.path.exists(mfile):
    sys.stderr.write(f"ERROR: Can not find specified sound file {mfile}! Check "
        "that the sound file exists in your package.\n")
    sys.exit(1)

def get_args():
    parser = argparse.ArgumentParser(description = __doc__)
    parser.add_argument(
        'method',
        metavar='[timer | stopwatch]',
        default='timer',
        choices=['timer', 'stopwatch'],
        help='Type of timer you want. A `timer` will count down from input '
            'hours, minutes, and / or seconds. A stopwatch will count up from '
            '0 until you press Ctrl+c to quit.'
    )
    parser.add_argument(
        '-t', '--tone',
        metavar='<tone>',
        help='Sound file to use for alarm when running in `timer` mode. The '
            'file must be in the MP3 format.'
    )
    parser.add_argument(
        '-s', '--settime',
        metavar = '<time>',
        help = 'Time in the format of hh:mm:ss for the `timer` function. You '
            'can leave out the seconds if you wish, but the hours and minutes '
            'are required. NOTE: Can now enter time in the format #h#m#s (e.g. '
            '1h5m30s) instead of 01:05:30 to make things a little easier to '
            'type. The old way may be deprecated.'
    )
    parser.add_argument(
        '-v', '--version',
        action = 'version', 
        version = '%(prog)s - v' + version
    )
    args = parser.parse_args()

    if args.method == 'timer' and args.settime is None:
        sys.stderr.write("ERROR: You must provide a set time in the format "
                "HH:MM:ss when using the `timer` function.\n")
        sys.exit(1)

    global mfile
    if args.tone:
        mfile = args.tone

    hours   = 0
    minutes = 0
    seconds = 0

    if args.settime:
        if any(x in ('h', 'm', 's') for x in args.settime):
            # We have the new h, m, s format for time (ex. 1m, 3m4s, 5h4m0s)
            elems = re.findall('\d+[hms]', args.settime)
            for e in elems:
                if e.endswith('h'):
                    hours = int(e.rstrip('h'))
                elif e.endswith('m'):
                    minutes = int(e.rstrip('m'))
                elif e.endswith('s'):
                    seconds = int(e.rstrip('s'))
        else:
            hours, minutes, seconds = map(int, args.settime.split(':'))
    return args.method, hours, minutes, seconds

def elapsed_time(time_start):
    """
    Count the elapsed time since starting. Kind of like a stop watch but not
    so precise.
    """
    hours   = 0
    minutes = 0
    seconds = 0

    while True:
        try:
            sys.stdout.write('\r{hours} Hours {minutes} Minutes {seconds} '
                'Seconds'.format(hours=hours, minutes=minutes, seconds=seconds))
            sys.stdout.flush()

            time.sleep(1)

            elapsed = int(time.time() - time_start)
            hours =   elapsed // 3600
            elapsed = elapsed - 3600 * hours
            minutes = elapsed // 60
            seconds = elapsed - (60 * minutes)
        except KeyboardInterrupt:
            break


def timer(time_start, hours, minutes, seconds):
    """
    Simple timer function.
    """
    target_seconds = (hours*3600 + minutes*60 + seconds)

    while int(time.time() - time_start) != target_seconds:
        #  print('{} <> {}'.format(int(time.time() - time_start), target_seconds))
        try:
            sys.stdout.write(f'\rTime Remaining: {hours:02}:{minutes:02}:{seconds:02}')
            sys.stdout.flush()

            time.sleep(1)

            elapsed = target_seconds - int(time.time() - time_start)
            #  print('\n{} <> {}'.format(elapsed, target_seconds))

            hours  = elapsed // 3600
            elapsed = elapsed - 3600 * hours
            minutes = elapsed // 60
            seconds = elapsed - (60 * minutes)
        except KeyboardInterrupt:
            sys.exit()

    sys.stdout.write("\nTime's up! ") 
    alarm()

def alarm():
    global mfile 

    pygame.mixer.init()
    pygame.mixer.music.load(mfile)
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.play(-1)

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
        if not input("Press ENTER to acknowledge alarm."):
            pygame.mixer.music.stop()
            sys.exit()

def main(method, hours, minutes, seconds):
    time_start = time.time()

    if method == 'stopwatch':
        print("Running stopwatch function. Press Ctrl + c to stop.")
        elapsed_time(time_start)
    else:
        print("Starting timer.")
        timer(time_start, hours, minutes, seconds)

if __name__ == '__main__':
    method, hours, minutes, seconds = get_args()
    try:
        main(method, hours, minutes, seconds)
    except KeyboardInterrupt:
        sys.exit(1)
