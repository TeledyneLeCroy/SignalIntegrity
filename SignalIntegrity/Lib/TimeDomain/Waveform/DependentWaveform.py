"""
StepWaveform.py
"""

# Copyright (c) 2018 Teledyne LeCroy, Inc.
# All rights reserved worldwide.
#
# This file is part of SignalIntegrity.
#
# SignalIntegrity is free software: You can redistribute it and/or modify it under the terms
# of the GNU General Public License as published by the Free Software Foundation, either
# version 3 of the License, or any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.
# If not, see <https://www.gnu.org/licenses/>

from SignalIntegrity.Lib.TimeDomain.Waveform.Waveform import Waveform
import math
import numpy as np

class DependentWaveform(Waveform):
    """step waveform"""
    def __init__(self, OutputPortName, TransformFN):
        """Constructor  
        constructs a dependent waveform, whose value depends on the measured output probe value through an arbitrary transform function. 
        @param outputPortName output port whose voltage is taken as input into transformation function
        @param transformFN file name of function which transforms ouptutPort's voltage into the new voltage of this waveform.
        """
        self.OutputPortName = OutputPortName
        self.TransformFN = TransformFN
        super().__init__()

    def UpdateWaveform(self, OutputWaveformLabels, OutputWaveformList):
        if (self.OutputPortName in OutputWaveformLabels):
            inputWaveform = OutputWaveformList[np.where(OutputWaveformLabels == self.OutputPortName)]
            #Todo - call file on function to take in that input 
            super().__init__(x=inputWaveform)
        else:
            #Todo - throw some kind of error
            print('ERROR: TO IMPLEMENT')