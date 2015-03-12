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

import subprocess

m_range = range(1, 11)
t_0_value = 100000
num_pu = 5
m_value = 5
iterations = 1
t_switch_value_range = [x * 0.1 for x in range(1,21)]
t_switch_value_range = [0.1]
t_switch_value_range += [x * 0.25 for x in range(1,11)]

print t_switch_value_range

print "M\tPU\tt_s\tVLow\tLow\tMedium\tHigh\tVHigh"
for t_switch_value in t_switch_value_range:
    subprocess.call(["./MobilitySim.py",
                                "-a", "verylow,low,medium,high,veryhigh",
                                "-q",
                                "-c",
                                "-m %d" % m_value,
                                "-t %d" % t_0_value,
                                "-s %.2f" % t_switch_value,
                                "-p %d" % num_pu,
                                "-i %d" % iterations])

