#!/usr/bin/env python
#
# This file is part of MobilitySim. MobilitySim is free software: you can
# redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright 2014 Andre Puschmann <andre.puschmann@tu-ilmenau.de>

import random
import simpy
import numpy as np
import sys
from optparse import OptionParser
from helper import *

RANDOM_SEED = 42
    
class Channel(object):
    def __init__(self, name):
        self.name = name
        self.users = []


class SecondaryUser(object):
    def __init__(self, env, name, channels, t_time, t_switch, verbose):
        self.env = env
        self.name = name
        self.channels = channels
        self.t_time = t_time # this is the time we need to transfer our data
        self.t_switch = t_switch # time needed to vacate a channel
        self.is_su = True
        self.finished = self.env.event()
        self.num_handover = 0
        self.end_time = 0
        self.verbose = verbose
        
        self.process = self.env.process(self.run())
               
    def transfer(self, time):
        yield self.env.timeout(time)

    def run(self):
        while True:
            # first check if we can find an idle channel
            channel = None
            for chan in self.channels:
                if not chan.users:
                    channel = chan

            # if still no channel is free, among the busy ones, select
            # one randomly and wait until this one gets idle
            if channel == None:
                channel = np.random.choice(self.channels)
                while channel.users:
                    yield channel.users[0].busy_over

            assert(len(channel.users) == 0)
            
            # from now on, the channel can be used
            channel.users.append(self) # tune to channel

            try:
                start = self.env.now
                yield self.env.process(self.transfer(self.t_time))
                if self.verbose: print('data transfer finished after %.2f on %s, %d handover needed in total' % (self.env.now, channel.name, self.num_handover))
                self.end_time = self.env.now
                channel.users.remove(self)
                yield self.finished.succeed() # trigger finished event

            except simpy.Interrupt as i:
                pu = i.cause
                if self.verbose: print('Handover forced, %s arrived on %s after %.2f' % (pu.name, channel.name, self.env.now - start))
                self.num_handover += 1
                
                # nodes has already been removed from channel (see PU)
                self.t_time = self.t_time - (self.env.now - start)
                if self.verbose: print('%s remaining transfer time %.2f' % (self.name, self.t_time))

                # switch to new channel
                yield self.env.timeout(self.t_switch)


class PrimaryUser(object):
    def __init__(self, env, name, channels, load, verbose):
        self.env = env
        self.name = name
        self.channels = channels
        self.load = load
        self.is_su = False
        self.busy_over = self.env.event()
        self.verbose = verbose
        
        self.process = self.env.process(self.run())

    def run(self):
        while True:
            channel = np.random.choice(self.channels)
            if self.verbose: print('%s tunes to %s' % (self.name, channel.name))
           
            # look for SU users and interrupt them
            for user in channel.users:               
                if user.is_su == True:
                    # force SU handover and interrupt
                    channel.users.remove(user)
                    user.process.interrupt(self)
            
            channel.users.append(self) # tune to channel
            
            # get length of next busy period
            busy_time = get_busy_period(self.load)                       
            if self.verbose: print('%s stays on %s for %.2f' % (self.name, channel.name, busy_time))
            
            yield self.env.timeout(busy_time)
            yield self.busy_over.succeed() # trigger over event to wake up SU (if any)
            
            self.busy_over = self.env.event() # rearm event
            channel.users.remove(self) # tune away from channel
            
            # get length of next idle period
            idle_time = get_idle_period(self.load)
            if self.verbose: print('%s is idle for %.2f' % (self.name, idle_time))
            yield self.env.timeout(idle_time)


def main():
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("-m", "--numchannels", dest="M", default=1,
                      help="How many channels are available (the M parameter)")
    parser.add_option("-t", "--time", dest="t_0", default="100000",
                      help="Transfer time in s")
    parser.add_option("-s", "--switchtime", dest="t_switch", default="1.5",
                      help="Time needed for SU to tune to another channel")
    parser.add_option("-p", "--numpus", dest="numpus", default=1,
                      help="How many PU")
    parser.add_option("-a", "--pumodel", dest="pumodel", default=["verylow"],
                      help="PU activity pattern (verylow, low, medium, high, veryhigh)",
                      type='string', action='callback', callback=string_splitter)
    parser.add_option("-i", "--iterations", dest="iterations", default=1,
                      help="How often to repeat the simulation")
    parser.add_option("-q", "--quiet",
                      action="store_false", dest="verbose", default=True,
                      help="don't print status messages to stdout")
    parser.add_option("-f", "--file", dest="file",
                      help="Write output to file", metavar="FILE")
    
    # turn command line parameters into local variables
    (options, args) = parser.parse_args()
    pumodels = options.pumodel
    M = int(options.M)
    t_0 = int(options.t_0)
    t_switch = float(options.t_switch)
    num_pus = int(options.numpus)
    iterations = int(options.iterations)
    verbose = options.verbose

    # Initialize seed, this helps reproducing the results
    np.random.seed(RANDOM_SEED)

    print("%d\t%d\t%.2f\t" % (M, num_pus, t_switch)),
    for model in pumodels:
        t_total = []    
        for run in range(iterations):           
            env = simpy.Environment()
            channels = [Channel('channel%d' % i) for i in range(M)]
            pus = [PrimaryUser(env, 'pu%d' % i, channels, model, verbose) for i in range(num_pus)]
            su = SecondaryUser(env, 'su1', channels, t_0, t_switch, verbose)
        
            #env.run()    
            #env.run(until=1000)
            env.run(until=su.finished)

            # accumulate total transfer times
            t_total.append(su.end_time)    

        # calculate aggregated efficiency
        eff = t_0 / np.mean(t_total)
        if verbose: print("Mean transfer time after %d iterations is %.2f, Eff: %.2f" % (len(t_total), np.mean(t_total), eff))
        print("%.2f\t" % eff),
    
    print ""


if __name__ == "__main__":
    main()
