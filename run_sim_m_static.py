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

m_range = range(1, 11) # M and PU range
t_0_value = 100000
t_switch_value = 1.5

iterations = 1

print "M\tPU\tt_s\tVLow\tLow\tMedium\tHigh\tVHigh"
for m_value in m_range:
    subprocess.call(["./MobilitySim.py",
                                "-a", "verylow,low,medium,high,veryhigh",
                                "-q",
                                "-c",
                                "-m %d" % m_value,
                                "-t %d" % t_0_value,
                                "-s %.2f" % t_switch_value,
                                "-p %d" % m_value,
                                "-i %d" % iterations])
