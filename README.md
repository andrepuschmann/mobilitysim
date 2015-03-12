MobilitySim
===========

This is the source code of a dynamic spectrum access (DSA) network simulation written
in Python using SimPy.
The purpose of this simulation is to evaluate the impact of spectrum mobility
functionality in overlay DSA networks.

The simulation framework assumes a pair of secondary user (SU) nodes that wish to transfer a certain
amount of data between each other. Thereby, the SUs access channels owned by a primary user (PU)
in an opportunistic manner. In other words, they can only use the communication resource
if the PU is not actively using it.

For modeling the activity of PUs, we use a model based on busy/idle patterns proposed by
Lopez-Benitez in a paper entitled "Time-Dimension Models of Spectrum Usage for the Analysis, Design, and Simulation of Cognitive Radio Networks" [[link]](http://ieeexplore.ieee.org/xpl/articleDetails.jsp?arnumber=6410055).

##Running the simulation

For running the simulation, one can just use one of the provided examples.
The simulation results are directly written to stdout as CSVs and could be piped into an extra
file for plotting.

```
./run_sim_m_static.py
M	PU	t_s	VLow	Low	Medium	High	VHigh
1	1	1.50	0.91	0.71	0.49	0.29	0.07	
2	2	1.50	0.97	0.83	0.58	0.33	0.06	
3	3	1.50	0.97	0.89	0.67	0.37	0.06	
4	4	1.50	0.98	0.90	0.73	0.42	0.07	
5	5	1.50	0.98	0.91	0.77	0.47	0.07	
6	6	1.50	0.98	0.91	0.80	0.51	0.07	
7	7	1.50	0.98	0.92	0.82	0.56	0.07	
8	8	1.50	0.98	0.91	0.82	0.59	0.07	
9	9	1.50	0.98	0.92	0.83	0.62	0.07	
10	10	1.50	0.98	0.91	0.83	0.65	0.08
```

##License and Referencing

This code package is licensed under the GPLv2 license. If you in any way use this code for research that results in publications, please cite our code.
