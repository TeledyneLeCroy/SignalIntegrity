"""
PreferencesFile.py
"""
# Copyright (c) 2021 Nubis Communications, Inc.
# Copyright (c) 2018-2020 Teledyne LeCroy, Inc.
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
from SignalIntegrity.App.ProjectFileBase import XMLConfiguration,XMLPropertyDefaultString,XMLPropertyDefaultInt,XMLPropertyDefaultBool,XMLPropertyDefaultFloat
from SignalIntegrity.App.ProjectFileBase import ProjectFileBase,XMLProperty
from SignalIntegrity.App.SParameterProperties import SParameterProperties

import os

class EyeYAxisConfiguration(XMLConfiguration):
    def __init__(self):
        super().__init__('YAxis')
        self.Add(XMLPropertyDefaultString('Mode','Auto'))
        self.Add(XMLPropertyDefaultFloat('Max',1.0))
        self.Add(XMLPropertyDefaultFloat('Min',0.0))

class EyeLogIntensityConfiguration(XMLConfiguration):
    def __init__(self):
        super().__init__('LogIntensity')
        self.Add(XMLPropertyDefaultBool('LogIntensity',False))
        self.Add(XMLPropertyDefaultFloat('MinExponent',-12))
        self.Add(XMLPropertyDefaultFloat('MaxExponent',0))

class EyeJitterNoiseConfiguration(XMLConfiguration):
    def __init__(self):
        super().__init__('JitterNoise')
        self.Add(XMLPropertyDefaultFloat('JitterS',0))
        self.Add(XMLPropertyDefaultFloat('JitterDeterministicPkS',0))
        self.Add(XMLPropertyDefaultFloat('Noise',0.0))
        self.Add(XMLPropertyDefaultInt('MaxKernelPixels',100000))
        self.SubDir(EyeLogIntensityConfiguration())

class EyeAlignmentConfiguration(XMLConfiguration):
    def __init__(self):
        super().__init__('Alignment')
        self.Add(XMLPropertyDefaultBool('AutoAlign',False))
        self.Add(XMLPropertyDefaultFloat('BERForAlignment',-3))
        self.Add(XMLPropertyDefaultInt('BitsPerSymbol',1))
        self.Add(XMLPropertyDefaultString('Mode','Horizontal')) # 'Horizontal' or 'Vertical'
        self.Add(XMLPropertyDefaultString('Horizontal','Middle')) # 'Middle' or 'Max' (vertical eye)
        self.Add(XMLPropertyDefaultString('Vertical','MaxMin')) # 'MaxMin' (maximum minimum opening) or 'Max' (maximum opening) 

class BathtubConfiguration(XMLConfiguration):
    def __init__(self):
        super().__init__('Bathtub')
        self.Add(XMLPropertyDefaultBool('Measure',False))
        self.Add(XMLPropertyDefaultFloat('DecadesFromJoinForFit',0.5))
        self.Add(XMLPropertyDefaultInt('MinPointsForFit',6))

class DecisionConfiguration(XMLConfiguration):
    def __init__(self):
        super().__init__('Decision')
        self.Add(XMLPropertyDefaultString('Mode','Mid')) # 'Mid' or 'Best' for independent decision levels

class EyeEnhancedPrecisionConfiguration(XMLConfiguration):
    def __init__(self):
        super().__init__('EnhancedPrecision')
        self.Add(XMLPropertyDefaultString('Mode','Auto'))
        self.Add(XMLPropertyDefaultInt('FixedEnhancement',10))

class EyeMeasureConfiguration(XMLConfiguration):
    def __init__(self):
        super().__init__('Measure')
        self.Add(XMLPropertyDefaultBool('Measure',False))
        self.Add(XMLPropertyDefaultString('WaveformType','V')) # 'V', 'A', 'W', 'FW', 'AW', 'VW'
        self.Add(XMLPropertyDefaultString('RxTx','Rx')) # 'Rx', 'Tx', 'N/A'
        self.Add(XMLPropertyDefaultBool('TxInputPowerAvailable',False))
        self.Add(XMLPropertyDefaultFloat('TxInputPowerW',0))
        self.Add(XMLPropertyDefaultFloat('TxInputPowerdBm',0,write=False))
        self.Add(XMLPropertyDefaultFloat('BERForMeasure',-6))

class EyeContourConfiguration(XMLConfiguration):
    def __init__(self):
        super().__init__('Contours')
        self.Add(XMLPropertyDefaultBool('Show',False))
        self.Add(XMLPropertyDefaultString('Which','Eye')) # 'Eye' or 'All'

class EyeAnnotationConfiguration(XMLConfiguration):
    def __init__(self):
        super().__init__('Annotation')
        self.Add(XMLPropertyDefaultBool('Annotate',False))
        self.Add(XMLPropertyDefaultString('Color','#ffffff'))
        self.Add(XMLPropertyDefaultBool('MeanLevels',True))
        self.Add(XMLPropertyDefaultBool('LabelMeanLevels',False))
        self.Add(XMLPropertyDefaultBool('LevelExtents',False))
        self.Add(XMLPropertyDefaultBool('EyeWidth',True))
        self.Add(XMLPropertyDefaultBool('EyeHeight',True))
        self.SubDir(EyeContourConfiguration())

class ClockRecoveryConfiguration(XMLConfiguration):
    def __init__(self):
        super().__init__('ClockRecovery')
        self.Add(XMLPropertyDefaultBool('Recover',False))
        self.Add(XMLPropertyDefaultInt('TrimLeftRight',20))

class EyeConfiguration(XMLConfiguration):
    def __init__(self):
        super().__init__('EyeDiagram')
        self.Add(XMLPropertyDefaultString('Color','#ffffff'))
        self.Add(XMLPropertyDefaultInt('UI',3))
        self.Add(XMLPropertyDefaultInt('Rows',200))
        self.Add(XMLPropertyDefaultInt('Columns',200))
        self.Add(XMLPropertyDefaultFloat('Saturation',20))
        self.Add(XMLPropertyDefaultFloat('ScaleX',75.))
        self.Add(XMLPropertyDefaultFloat('ScaleY',150.))
        self.Add(XMLPropertyDefaultString('Mode','ISI'))
        self.Add(XMLPropertyDefaultBool('Invert',True))
        self.SubDir(ClockRecoveryConfiguration())
        self.SubDir(EyeYAxisConfiguration())
        self.SubDir(EyeJitterNoiseConfiguration())
        self.SubDir(EyeAlignmentConfiguration())
        self.SubDir(EyeEnhancedPrecisionConfiguration())
        self.SubDir(EyeMeasureConfiguration())
        self.SubDir(EyeAnnotationConfiguration())
        self.SubDir(DecisionConfiguration())
        self.SubDir(BathtubConfiguration())

class DeviceConfigurations(XMLConfiguration):
    def __init__(self):
        super().__init__('Devices')
        self.SubDir(EyeConfiguration())

class Color(XMLConfiguration):
    def __init__(self):
        XMLConfiguration.__init__(self,'Color')
        self.Add(XMLPropertyDefaultString('Background'))
        self.Add(XMLPropertyDefaultString('Foreground'))
        self.Add(XMLPropertyDefaultString('ActiveBackground'))
        self.Add(XMLPropertyDefaultString('ActiveForeground'))
        self.Add(XMLPropertyDefaultString('DisabledForeground'))
        self.Add(XMLPropertyDefaultString('Plot'))

class Appearance(XMLConfiguration):
    def __init__(self):
        XMLConfiguration.__init__(self,'Appearance')
        self.Add(XMLPropertyDefaultInt('FontSize',12))
        self.Add(XMLPropertyDefaultInt('InitialGrid',16))
        self.Add(XMLPropertyDefaultFloat('PlotWidth',5))
        self.Add(XMLPropertyDefaultFloat('PlotHeight',2))
        self.Add(XMLPropertyDefaultInt('PlotDPI',100))
        self.Add(XMLPropertyDefaultBool('PlotCursorValues',False))
        self.Add(XMLPropertyDefaultBool('AllPinNumbersVisible',False))
        self.Add(XMLPropertyDefaultBool('GridsOnPlots',True))
        self.Add(XMLPropertyDefaultInt('RoundDisplayedValues',4))
        self.Add(XMLPropertyDefaultInt('LimitText',60))
        self.SubDir(Color())

class Variables(XMLConfiguration):
    def __init__(self):
        super().__init__('Variables')
        self.Add(XMLPropertyDefaultBool('ParameterizeOnlyVisible',True))

class Calculation(XMLConfiguration):
    def __init__(self):
        XMLConfiguration.__init__(self,'Calculation')
        self.Add(XMLPropertyDefaultBool('TrySVD',True))
        self.Add(XMLPropertyDefaultBool('CheckConditionNumber',True))
        self.Add(XMLPropertyDefaultBool('UseSinX',True))
        self.Add(XMLPropertyDefaultBool('Enforce12458',True))
        self.Add(XMLPropertyDefaultFloat('MaximumWaveformSize',5e6))
        self.Add(XMLPropertyDefaultBool('MultiPortTee',True))
        self.Add(XMLPropertyDefaultBool('IgnoreMissingOtherWaveforms',True))
        self.Add(XMLPropertyDefaultBool('LogarithmicSolutions',False))
        self.Add(XMLPropertyDefaultBool('Non50OhmSolutions',False))
        self.Add(XMLPropertyDefaultBool('AutoshutoffIterations', False))
        self.Add(XMLPropertyDefaultFloat('AutoshutoffThreshold', 1E-3))
    def ApplyPreferences(self):
        import SignalIntegrity.Lib as si
        si.td.wf.Waveform.adaptionStrategy='SinX' if self['UseSinX'] else 'Linear'
        si.td.wf.Waveform.maximumWaveformSize = self['MaximumWaveformSize']
        si.sd.Numeric.trySVD=self['TrySVD']
        si.sd.Numeric.checkConditionNumber=self['CheckConditionNumber']
        si.p.SystemDescriptionParser.MultiPortTee=self['MultiPortTee']

class Cache(XMLConfiguration):
    def __init__(self):
        XMLConfiguration.__init__(self,'Cache')
        self.Add(XMLPropertyDefaultBool('CacheResults',True))

class LastFiles(XMLConfiguration):
    def __init__(self):
        XMLConfiguration.__init__(self,'LastFiles')
        self.Add(XMLPropertyDefaultString('Name'))
        self.Add(XMLPropertyDefaultString('Directory'))

class Encryption(XMLConfiguration):
    def __init__(self):
        XMLConfiguration.__init__(self,'Encryption')
        self.Add(XMLPropertyDefaultString('Password',''))
        self.Add(XMLPropertyDefaultString('Ending','$'))
    def ApplyPreferences(self):
        from SignalIntegrity.App.Encryption import Encryption
        Encryption(pwd=self['Password'],ending=self['Ending'])

class ProjectFiles(XMLConfiguration):
    def __init__(self):
        XMLConfiguration.__init__(self,'ProjectFiles')
        self.Add(XMLPropertyDefaultBool('OpenLastFile',True))
        self.Add(XMLPropertyDefaultBool('RetainLastFilesOpened',True))
        self.Add(XMLProperty('LastFile',[LastFiles() for _ in range(4)],'array',arrayType=LastFiles()))
        self.Add(XMLPropertyDefaultBool('AskToSaveCurrentFile',True))
        self.Add(XMLPropertyDefaultBool('PreferSaveWaveformsLeCroyFormat',False))
        self.Add(XMLPropertyDefaultBool('PlotAllIterations', False))
        self.SubDir(Encryption())

class OnlineHelp(XMLConfiguration):
    def __init__(self):
        XMLConfiguration.__init__(self,'OnlineHelp')
        self.Add(XMLPropertyDefaultBool('UseOnlineHelp',True))
        self.Add(XMLPropertyDefaultString('URL','https://nubis-communications.github.io/SignalIntegrity/SignalIntegrity/App'))

class Features(XMLConfiguration):
    def __init__(self):
        XMLConfiguration.__init__(self,'Features')
        self.Add(XMLPropertyDefaultBool('NetworkAnalyzerModel',False))

class PreferencesFile(ProjectFileBase):
    def __init__(self):
        ProjectFileBase.__init__(self)
        self.Add(XMLPropertyDefaultString('Version',None))
        self.SubDir(ProjectFiles())
        self.SubDir(Appearance())
        self.SubDir(Cache())
        self.SubDir(OnlineHelp())
        self.SubDir(Calculation())
        self.SubDir(SParameterProperties(preferences=True))
        self.SubDir(DeviceConfigurations())
        self.SubDir(Variables())
        self.SubDir(Features())
    def ApplyPreferences(self):
        self['Calculation'].ApplyPreferences()
        self['ProjectFiles.Encryption'].ApplyPreferences()

