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

# This file includes some helper scripts for MobilitySim that are
# used to generate realistic PU activity patterns.
# 
# Those busy/idle patterns are based on the work of Miguel Lopez-Benitez:
# "Time-Dimension Models of Spectrum Usage for the Analysis, Design, and Simulation of Cognitive Radio Networks"
# [[link]](http://ieeexplore.ieee.org/xpl/articleDetails.jsp?arnumber=6410055)

import random

# dictionary with GPD parameters as dictionary
loads = {}
loads['verylow'] = {'busy_mu': 3.5150,
                    'busy_sigma': 1.6960,
                    'busy_xi': 0.0285,
                    'idle_mu': 3.61,
                    'idle_sigma': 38.3633,
                    'idle_xi': 0.2125 }
loads['low'] = {'busy_mu': 3.5150,
                    'busy_sigma': 2.6240,
                    'busy_xi': 0.1884,
                    'idle_mu': 3.578,
                    'idle_sigma': 10.9356,
                    'idle_xi': 0.1784 }                    
loads['medium'] = {'busy_mu': 3.5150,
                    'busy_sigma': 5.1483,
                    'busy_xi': 0.1978,
                    'idle_mu': 3.5160,
                    'idle_sigma': 4.6583,
                    'idle_xi': 0.2156 }
loads['high'] = {'busy_mu': 3.5470,
                    'busy_sigma': 10.7968,
                    'busy_xi': 0.1929,
                    'idle_mu': 3.5310,
                    'idle_sigma': 2.6272,
                    'idle_xi': 0.2119 }
loads['veryhigh'] = {'busy_mu': 3.5940,
                    'busy_sigma': 52.8611,
                    'busy_xi': 0.2377,
                    'idle_mu': 3.5160,
                    'idle_sigma': 1.6609,
                    'idle_xi': 0.0068 }

# mu is location
# sigma is scale
# xi is shape
# U is input
# X = mu + sigma(U^-xi - 1) / xi  (http://en.wikipedia.org/wiki/Generalized_Pareto_distribution)
def gpd_cdf_invers(mu, sigma, xi, U):
    e1 = U ** (-xi) - 1
    e2 = sigma * e1 / xi
    return mu + e2

def get_busy_period(load):
    u = random.uniform(0, 1)
    return gpd_cdf_invers(loads[load]['busy_mu'], loads[load]['busy_sigma'], loads[load]['busy_xi'], u)

def get_idle_period(load):
    u = random.uniform(0, 1)
    return gpd_cdf_invers(loads[load]['idle_mu'], loads[load]['idle_sigma'], loads[load]['idle_xi'], u)
    
def string_splitter(option, opt, value, parser):
    setattr(parser.values, option.dest, value.split(','))
