from SignalIntegrity.Lib.TimeDomain.Waveform.Waveform import Waveform

#Code which will be run by a dependent voltage source to perform voltage transformation
#This simple explanation will just scale the input waveform
# inpputs: inputWaveform - contains Waveform to utilize
# outputs: outputWaveform - set to transformed Waveform

#Check if scale variable initialized (passed in)
if 'scale' in systemVars:
    scale = float(systemVars['scale'])
    print('Read in scale facto from system var')
else:
    scale = 2
    print('Default scale factor')
outputWaveform = inputWaveform*scale
print('RAN IT')


