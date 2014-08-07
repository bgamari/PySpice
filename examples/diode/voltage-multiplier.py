# -*- coding: utf-8 -*-

#!# This example shows a voltage multiplier using diodes and capacitors.
#!# See ` <http://en.wikipedia.org/wiki/Voltage_multiplier>`_

####################################################################################################

import os

import matplotlib.pyplot as plt

####################################################################################################

import PySpice.Logging.Logging as Logging
logger = Logging.setup_logging()

####################################################################################################

from PySpice.Probe.Plot import plot
from PySpice.Spice.Library import SpiceLibrary
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit.Units import *

####################################################################################################

libraries_path = os.path.join(os.environ['PySpice_examples_path'], 'libraries')
spice_library = SpiceLibrary(libraries_path)

####################################################################################################

circuit = Circuit('Voltage Multiplier')
circuit.include(spice_library['1N4148'])
source = circuit.Sinusoidal('input', 1, circuit.gnd, amplitude=10, frequency=50)

multiplier = 5
for i in xrange(multiplier):
    # It is easier in the loop to permute the ground and the input node
    circuit.C(i, i, i+2, milli(1))
    circuit.X(i, '1N4148', i+2, i+1)
circuit.R(1, multiplier, multiplier+1, mega(1))

simulator = circuit.simulator(temperature=25, nominal_temperature=25)
analysis = simulator.transient(step_time=source.period/200, end_time=source.period*20,
                               probes=['V({})'.format(i) for i in xrange(multiplier +2)])

####################################################################################################

figure = plt.figure(1, (20, 10))

axe = plt.subplot(111)
axe.set_title('Voltage Multiplier')
axe.set_xlabel('Time [s]')
axe.set_ylabel('Voltage [V]')
axe.grid()
# Fixme: axis vs axe ...
for i in xrange(1, multiplier+2):
    y = analysis[str(i)]
    if i != 1 and i & 1: # odd, i = 1 is source
        y -= analysis['1']
    plot(y, axis=axe)
# axe.axhline(-multiplier*source.amplitude)
axe.set_ylim(-multiplier*1.1*source.amplitude, 1.1*source.amplitude)
axe.legend(['input'] + ['*{}'.format(i-1) for i in xrange(2, multiplier +2)] ,
           loc=(.2,.8))

plt.tight_layout()
plt.show()

#fig# save_figure(figure, 'voltage-multiplier.png')

####################################################################################################
# 
# End
# 
####################################################################################################