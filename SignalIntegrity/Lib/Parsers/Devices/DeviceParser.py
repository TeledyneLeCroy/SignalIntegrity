"""
DeviceParser.py
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
from numpy import zeros
import copy

class ParserDevice(object):
    """class defining how to parse devices"""
    def __init__(self,devicename,ports,arginname,defaults,frequencyDependent,func):
        """Constructor
        @param devicename string name of device
        @param ports integer or string number of ports in device or None.  If a string, then the string
        is either a comma separated list of possible numbers of ports or is two numbers separated
        by a - indicating a range of numbers of ports.  If None, then the device can have
        any number of ports.
        @param arginname boolean whether the first argument requires a keyword or not.  Simple
        things like resistors and capacitors just have their value after the device and ports
        declaration.  This is False if the device has no arguments.
        @param defaults dictionary containing keyword/default value pairs.  if arginname is True
        then one arguments keyword will be the empty string ''.
        @param frequencyDependent boolean whether the device is frequency dependent.
        @param func string that when evaluated will be the device.  
        """
        self.devicename=devicename
        self.ports=ports
        self.arginname=arginname
        defaults['z0']=50.
        self.defaults=defaults
        self.frequencyDependent=frequencyDependent
        self.func=func

class DeviceFactory(list):
    """device class factory that produces devices"""
    def __init__(self):
        """Constructor
        list of devices
        todo: fill in reference impedance arguments in table
        | name                                  |ports|arginname| defaults                                                                                      |frequency\n dependent|device                                                                                           |
        |:-------------------------------------:|:---:|:-------:|:---------------------------------------------------------------------------------------------:|:-------------------:|:------------------------------------------------------------------------------------------------|
        |file                                   |any  |True     |filename=None                                                                                  | True                |sp.dev.SParameterFile(filename,50.,callback)                                                     |
        |c                                      |1    |True     |c=None df=0 esr=0 z0=50                                                                        | True                |sp.dev.TerminationC(f,c,z0,df,esr)                                                               |
        |c                                      |2    |True     |c=None df=0 esr=0 z0=50                                                                        | True                |sp.dev.SeriesC(f,c,z0,df,esr)                                                                    |
        |l                                      |1    |True     |l=None                                                                                         | True                |sp.dev.TerminationL(f,l,z0)                                                                      |
        |l                                      |2    |True     |l=None                                                                                         | True                |sp.dev.SeriesL(f,l,z0)                                                                           |
        |r                                      |1    |True     |r=None                                                                                         | False               |dev.TerminationZ(r)                                                                              |
        |r                                      |2    |True     |r=None                                                                                         | False               |dev.SeriesZ(r)                                                                                   |
        |rse                                    |2    |True     |r=None                                                                                         | True                |sp.dev.SeriesRse(r)                                                                              |
        |shunt                                  |2-4  |True     |r=None                                                                                         | False               |dev.ShuntZ(ports,r)                                                                              |
        |m                                      |4    |True     |m=None                                                                                         | True                |sp.dev.Mutual(f,m)                                                                               |
        |ground                                 |1    |False    |                                                                                               | False               |dev.Ground()                                                                                     |
        |open                                   |1    |False    |                                                                                               | False               |dev.Open()                                                                                       |
        |thru                                   |2    |False    |                                                                                               | False               |dev.Thru()                                                                                       |
        |directional\n coupler                  |3-4  |False    |                                                                                               | False               |dev.DirectionalCoupler(ports)                                                                    |
        |termination                            |any  |False    |                                                                                               | False               |zeros(shape=(ports,ports)).tolist()                                                              |
        |tee                                    |any  |False    |                                                                                               | False               |dev.Tee(ports)                                                                                   |
        |mixedmode                              |4    |True     |'power'                                                                                        | False               |dev.MixedModeConverter()\n or dev.MixedModeConverterVoltage()                                    |
        |ideal\n transformer                    |4    |True     |tr=1                                                                                           | False               |dev.IdealTransformer(tr)                                                                         |
        |voltage\n controlled\n voltage\n source|4    |True     |gain=None                                                                                      | False               |dev.VoltageControlledVoltageSource(gain)                                                         |
        |current\n controlled\n current\n source|4    |True     |gain=None                                                                                      | False               |dev.CurrentControlledCurrentSource(gain)                                                         |
        |current\n controlled\n voltage\n source|4    |True     |gain=None                                                                                      | False               |dev.CurrentControlledVoltageSource(gain)                                                         |
        |voltage\n controlled\n current\n source|4    |True     |gain=None                                                                                      | False               |dev.VoltageControlledCurrentSource(gain)                                                         |
        |voltage\n amplifier                    |2-4  |False    |gain=None zo=0 zi=1e8 z0=50                                                                    | False               |dev.VoltageAmplifier(ports,gain,zi,zo)                                                           |
        |current\n amplifier                    |2-4  |False    |gain=None zo=1e8 zi=0 z0=50                                                                    | False               |dev.CurrentAmplifier(ports,gain,zi,zo)                                                           |
        |transresistance\n amplifier            |2-4  |False    |gain=None zo=0 zi=0 z0=50                                                                      | False               |dev.TransresistanceAmplifier(ports,gain,zi,zo)                                                   |
        |transconductance\n amplifier           |2-4  |False    |gain=None zo=1e8 zi=1e8 z0=50                                                                  | False               |dev.TransconductanceAmplifier(ports,gain,zi,zo)                                                  |
        |opamp                                  |3    |False    |zi=1e8 zd=1e8 zo=0 gain=1e8 z0=50                                                              | False               |dev.OperationalAmplifier(zi,zd,zo,gain,z0)                                                       |
        |tline                                  |2,4  |False    |zc=50 td=0                                                                                     | True                |sp.dev.TLineLossless(f,ports,zc,td)                                                              |
        |tlineCOM                               |2    |False    |gamma0=0 a1=0 a2=0 tau=0 zc=50 d=0 z0=50                                                       | True                |sp.dev.TLineTwoPortCOM(f,gamma0,a1,a2,tau,zc,d/1e-3,z0)                                       |
        |tlinelossy                             |2    |False    |zc=50 td=0 LdBperHzpers=0 LdBperrootHzpers=0                                                   | True                |sp.dev.TLineLossy(f,ports,zc,td,LdBperHzpers,LdBperrootHzpers)                                   |
        |telegrapher                            |2    |False    |r=0 rse=0 l=0 c=0 df=0 g=0 z0=50 sect=0                                                        | True                |sp.dev.TLineTwoPortRLGC(\n f,r,rse,l,g,c,df,z0,sect,scale)                                       |
        |telegrapher                            |4    |False    |rp=0 rsep=0 lp=0 cp=0\n dfp=0 gp=0 rn=0 rsen=0\n ln=0 cn=0 dfn=0 gn=0\n lm 0 gm=0 z0=50\n scale=1.0 sect=0 | True    |sp.dev.TLineDifferentialRLGC(\n f,rp,rsep,lp,gp,cp,dfp,\n rn,rsen,ln,gn,cn,dfn,\n cm,dfm,gm,lm,z0,sect,scale) |
        |rlgcfit                                |2    |False    |file=None scale=1.0 z0=50                                                                      | True                |fit.RLGCFitFromFile(f,file,scale,Z0)                                                             |
        |w                                      |2-16 |True     |filename=None df=0 scale=1.0 sect=0                                                            | True                |sp.dev.WElementFile(f,filename,df,50.,sect,scale)                                                |
        |shortstd                               |1    |False    |od=0 oz0=50 ol=0 f0=1e9\n l0=0 l1=0.0 l2=0 l3=0                                                | True                |m.calkit.std.ShortStandard(f,od,oz0,ol,f0,l0,l1,l2,l3)                                           |
        |openstd                                |1    |False    |od=0 oz0=50 ol=0 f0=1e9\n c0=0 c1=0 c2=0 c3=0                                                  | True                |m.calkit.std.OpenStandard(f,od,oz0,ol,f0,c0,c1,c2,c3)                                            |
        |loadstd                                |1    |False    |od=0 oz0=50 ol=0 f0=1e9 tz=50                                                                  | True                |m.calkit.std.LoadStandard(f,od,oz0,ol,f0,tz0)                                                    |
        |thrustd                                |2    |False    |od=0 oz0=50 ol=0 f0=1e9                                                                        | True                |m.calkit.std.ThruStandard(f,od,oz0,ol,f0)                                                        |
        |networkanalyzer                        |any  |False    |file=None, et=None, pl=None, cd=calculate                                                      | True                |m.cal.NetworkAnalyzer(f,file,et,pl,not cd=='uncalculate')                                        |
        |bessellp                               |2    |False    |order=4 fc=None                                                                                | True                |sp.dev.BesselLowPassFilter(f,order,fc,50.)                                                       |
        |butterworthlp                          |2    |False    |order=4 fc=None                                                                                | True                |sp.dev.BesselLowPassFilter(f,order,fc,50.)                                                       |
        |ctle                                   |2    |False    |gdc=None gdc2=None fz=None flf=None fp1=None fp2=None                                          | True                |sp.dev.CTLE(f,gdc,gdc2,fz,flf,fp1,fp2,50.)                                                       |
        |ffe                                    |2    |True     |taps='[1.0]' td=None pre=0                                                                     | True                |sp.dev.FFE(f,td,taps,pre,50.)                                                                    |
        |laplace                                |2    |True     |eq                                                                                             | True                |sp.dev.Laplace(f,eq)                                                                             |
        |relay                                  |2-16 |True     |pos=0 term=1e9 Z0=50                                                                           | False               |dev.IdealRelay(ports,pos,term,z0)                                                                |
        |impulseresponsefilter                  |2    |True     |filename=None wfprojname=None dcGain=None mulTs=True derivative=False                          | True                |sp.dev.ImpulseResponseFilter(f,filename,dcGain,mulTs,derivative                                  |
        |parallel                               |2    |False    |filename=None sect=None                                                                        | True                |sp.dev.Parallel(f,file,sect,50.)                                                                 |
        @note ports any mean None supplied. comma or dash separated ports are supplied as a string.
        @note arginname means the argument is supplied without a keyword.  The first default argument has the actual name of the argument.
        @note frequency dependent devices usually come from 'sp.dev' meaning SParameters.Devices package.  Devices that are not frequency dependent
        come from 'dev' meaning devices.  'm.calkit.std' refers to 'Measurement.CalKit.Standards' package.
        @note Usually when an argument is defaulted to None, the device production will fail if the argument is not supplied - meaning the default value cannot be used.
        """
        list.__init__(self,[
        ParserDevice('file',None,True,{'':None},True,"SParameterFile(arg['']\
            ,None,callback,**extraArgs).Resample(f).\
            SetReferenceImpedance(float(arg['z0']))"),
        ParserDevice('c',1,True,{'':None,'df':0.,'esr':0.},True,
            "TerminationC(f,float(arg['']),float(arg['z0']),\
            float(arg['df']),float(arg['esr']))"),
        ParserDevice('c',2,True,{'':None,'df':0.,'esr':0.},True,
            "SeriesC(f,float(arg['']),float(arg['z0']),float(arg['df']),\
            float(arg['esr']))"),
        ParserDevice('l',1,True,{'':None},True,
                     "TerminationL(f,float(arg['']),float(arg['z0']))"),
        ParserDevice('l',2,True,{'':None},True,
                     "SeriesL(f,float(arg['']),float(arg['z0']))"),
        ParserDevice('r',1,True,{'':None},False,
                     "TerminationZ(float(arg['']),Z0=float(arg['z0']))"),
        ParserDevice('r',2,True,{'':None},False,
                     "SeriesZ(float(arg['']),Z0=float(arg['z0']))"),
        ParserDevice('rse',2,True,{'':None},True,
                     "SeriesRse(f,float(arg['']),Z0=float(arg['z0']))"),
        ParserDevice('shunt','2-4',True,{'':None},False,
            "ShuntZ(ports,float(arg['']),Z0=float(arg['z0']))"),
        ParserDevice('m',4,True,{'':None},True,
                     "Mutual(f,float(arg['']),Z0=float(arg['z0']))"),
        ParserDevice('ground',1,False,{},False,"Ground()"),
        ParserDevice('open',1,False,{},False,"Open()"),
        ParserDevice('thru',2,False,{},False,"Thru()"),
        ParserDevice('directionalcoupler','3-4',False,{},False,
            "DirectionalCoupler(ports)"),
        ParserDevice('termination',None,False,{},False,
            "zeros(shape=(ports,ports)).tolist()"),
        ParserDevice('tee',None,False,{},False,"Tee(ports)"),
        ParserDevice('mixedmode',4,True,{'':'power'},False,
            "(MixedModeConverterVoltage() if arg[''] == 'voltage'\
            else MixedModeConverter())"),
        ParserDevice('idealtransformer',4,True,{'':1.},False,
            "IdealTransformer(float(arg['']))"),
        ParserDevice('voltagecontrolledvoltagesource',4,True,{'':None},False,
            "VoltageControlledVoltageSource(float(arg['']))"),
        ParserDevice('currentcontrolledcurrentsource',4,True,{'':None},False,
            "CurrentControlledCurrentSource(float(arg['']))"),
        ParserDevice('currentcontrolledvoltagesource',4,True,{'':None},False,
            "CurrentControlledVoltageSource(float(arg['']),Z0=float(arg['z0']))"),
        ParserDevice('voltagecontrolledcurrentsource',4,True,{'':None},False,
            "VoltageControlledCurrentSource(float(arg['']),Z0=float(arg['z0']))"),
        ParserDevice('voltageamplifier','2-4',False,{'gain':None,'zo':0,'zi':1e8},
            False,"VoltageAmplifier(ports,float(arg['gain']),\
            float(arg['zi']),float(arg['zo']),Z0=float(arg['z0']))"),
        ParserDevice('currentamplifier','2-4',False,{'gain':None,'zo':1e8,'zi':0},
            False,"CurrentAmplifier(ports,float(arg['gain']),\
            float(arg['zi']),float(arg['zo']),Z0=float(arg['z0']))"),
        ParserDevice('transresistanceamplifier','2-4',False,{'gain':None,'zo':0.,
            'zi':0.},False,"TransresistanceAmplifier(ports,\
            float(arg['gain']),float(arg['zi']),float(arg['zo']),\
            Z0=float(arg['z0']))"),
        ParserDevice('transconductanceamplifier','2-4',False,{'gain':None,'zo':1e8,
            'zi':1e8},False,"TransconductanceAmplifier(ports,\
            float(arg['gain']),float(arg['zi']),float(arg['zo']),\
            Z0=float(arg['z0']))"),
        ParserDevice('opamp',3,False,{'zi':1e8,'zd':1e8,'zo':0.,'gain':1e8},
            False,"OperationalAmplifier(float(arg['zi']),float(arg['zd']),\
            float(arg['zo']),float(arg['gain']),float(arg['z0']))")])
        # pragma: silent exclude
        self.__init__Contd()
        # pragma: include
    def __init__Contd(self):
        list.__init__(self,list(self+[
        ParserDevice('tline','2,4',False,{'zc':50.,'td':0.},True,
            "TLineLossless(f,ports,float(arg['zc']),float(arg['td']),\
            Z0=float(arg['z0']))"),
        ParserDevice('tlinecom',2,False,{'gamma0':0,'a1':0,'a2':0,'tau':0,'zc':50,
            'd':0,'z0':50},True,
            "TLineTwoPortCOM(f,float(arg['gamma0']),float(arg['a1']),\
            float(arg['a2']),float(arg['tau']),float(arg['zc']),\
            float(arg['d'])/1e-3,float(arg['z0']))"),
        ParserDevice('tlinelossy',2,False,{'zc':50.,'td':0.,'ldbperhzpers':0,
            'ldbperroothzpers':0},True,
            "TLineLossy(f,float(arg['zc']),float(arg['td']),\
            float(arg['ldbperhzpers']),float(arg['ldbperroothzpers']),\
            Z0=float(arg['z0']))"),
        ParserDevice('telegrapher',2,False,{'r':0.,'rse':0.,'l':0.,'c':0.,'df':0.,
            'g':0.,'sect':0,'scale':1.},True,"TLineTwoPortRLGC(f,\
            float(arg['r']),float(arg['rse']),float(arg['l']),float(arg['g']),\
            float(arg['c']),float(arg['df']),float(arg['z0']),int(arg['sect']),\
            float(arg['scale']))"),
        ParserDevice('telegrapher',4,False,{'rp':0.,'rsep':0.,'lp':0.,'cp':0.,'dfp':0.,
            'gp':0.,'rn':0.,'rsen':0.,'ln':0.,'cn':0.,'dfn':0.,'gn':0.,'lm':0.,
            'cm':0.,'dfm':0.,'gm':0.,'sect':0,'scale':1.},
            True,"TLineDifferentialRLGC(f, float(arg['rp']),float(arg['rsep']),\
            float(arg['lp']),float(arg['gp']),float(arg['cp']),float(arg['dfp']),\
            float(arg['rn']),float(arg['rsen']),float(arg['ln']),float(arg['gn']),\
            float(arg['cn']),float(arg['dfn']),float(arg['cm']),float(arg['dfm']),\
            float(arg['gm']),float(arg['lm']),float(arg['z0']),int(arg['sect']),\
            float(arg['scale']))"),
        ParserDevice('rlgcfit',2,False,{'file':None,'scale':1},True,
            "RLGCFitFromFile(f,arg['file'],scale=float(arg['scale']),\
            Z0=float(arg['z0']),**extraArgs)"),
        ParserDevice('w','2,4,6,8,10,12,14,16',True,{'':None,'df':0.,'sect':0,
            'scale':1.},True,"WElementFile(f,arg[''],float(arg['df']),\
            float(arg['z0']),int(arg['sect']),float(arg['scale']))"),
        ParserDevice('shortstd',1,False,{'od':0.,'oz0':50.,'ol':0.0,'f0':1e9,
            'l0':0.0,'l1':0.0,'l2':0.0,'l3':0.0},True,
            "ShortStandard(f,float(arg['od']),float(arg['oz0']),float(arg['ol']),\
            float(arg['f0']),float(arg['l0']),float(arg['l1']),float(arg['l2']),\
            float(arg['l3']),Z0=float(arg['z0']))"),
        ParserDevice('openstd',1,False,{'od':0.,'oz0':50.,'ol':0.0,'f0':1e9,
            'c0':0.0,'c1':0.0,'c2':0.0,'c3':0.0},True,
            "OpenStandard(f,float(arg['od']),float(arg['oz0']),float(arg['ol']),\
            float(arg['f0']),float(arg['c0']),float(arg['c1']),float(arg['c2']),\
            float(arg['c3']),Z0=float(arg['z0']))"),
        ParserDevice('loadstd',1,False,{'od':0.,'oz0':50.,'ol':0.0,'f0':1e9,'tz':50.0},
            True,"LoadStandard(f,float(arg['od']),float(arg['oz0']),float(arg['ol']),\
            float(arg['f0']),float(arg['tz']),Z0=float(arg['z0']))"),
        ParserDevice('thrustd',2,False,{'od':0.,'oz0':50.,'ol':0.0,'f0':1e9},
            True,"ThruStandard(f,float(arg['od']),float(arg['oz0']),float(arg['ol']),\
            float(arg['f0']),Z0=float(arg['z0']))")
        ]))
        # pragma: silent exclude
        self.__init__Contd2()
        # pragma: include
    def __init__Contd2(self):
        list.__init__(self,list(self+[
        ParserDevice('networkanalyzer',None,False,{'file':None,'et':None,'pl':None,
            'cd':'calculate'},True,"NetworkAnalyzer(f,arg['file'],arg['et'],arg['pl'],\
            (not arg['cd']=='uncalculate'),callback,**extraArgs)"),
        ParserDevice('dut',None,True,{'':None},True,"SParameterFile(arg[''],\
            None,callback,**extraArgs).Resample(f).SetReferenceImpedance(float(arg['z0']))"),
        ParserDevice('bessellp',2,False,{'order':4,'fc':None},True,
            "BesselLowPassFilter(f,int(arg['order']),float(arg['fc']),Z0=float(arg['z0']))"),
        ParserDevice('butterworthlp',2,False,{'order':4,'fc':None},True,
            "ButterworthLowPassFilter(f,int(arg['order']),float(arg['fc']),\
            Z0=float(arg['z0']))"),
        ParserDevice('ctle',2,False,{'gdc':None,'gdc2':None,'fz':None,'flf':None,
            'fp1':None,'fp2':None},True,"CTLE(f,float(arg['gdc']),float(arg['gdc2']),\
            float(arg['fz']),float(arg['flf']),float(arg['fp1']),float(arg['fp2']),\
            Z0=float(arg['z0']))"),
        ParserDevice('ffe',2,True,{'':'[1.0]','td':None,'pre':0},True,"FFE(f,\
            float(arg['td']),eval(arg['']),eval(arg['pre']),Z0=float(arg['z0']))"),
        ParserDevice('laplace',2,True,{'':''},True,"Laplace(f,str(arg['']),\
            Z0=float(arg['z0']))"),
        ParserDevice('relay','2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17',True,{'':0,'term':1e9},
            False,"IdealRelay(ports,int(arg['']),float(arg['term']),float(arg['z0']))"),
        ParserDevice('impulseresponsefilter',2,True,
            {'':None,'wfprojname':'None','dcgain':None,'mults':True,'derivative':False},True,
            "ImpulseResponseFilter(arg[''],wfProjName=arg['wfprojname'],\
            normalizedDCGain=eval(arg['dcgain']),multiplyByTs=(arg['mults']=='true'),\
            derivative=(arg['derivative']=='true'),**extraArgs).Resample(f)"),
        ParserDevice('parallel',2,False,{'file':None,'sect':None},True,
                     "Parallel(f,arg['file'],int(arg['sect']),float(arg['z0']),**extraArgs)")
        ]))
    def MakeDevice(self,ports,callback, argsList, f, Z0=50.):
        """makes a device from a set of arguments
        The device is assigned to self.dev and self.frequencyDependent determines whether the
        device is frequency dependent.  Frequency dependent devices are assumed to be instances
        of the class SParameters.  Otherwise, they are list of list matrices.

        @param ports integer number of ports
        @param argsList list of arguments.  The name of the device is the first argument.
        If the device has no keyword for the argument, then that argument is next.  Otherwise, besides
        the name and the argument with no keyword, the remaining arguments come in keyword/value pairs where the
        keyword is a string and the value is the value of the keyword.
        @param f list of frequencies
        @param Z0 float (optional, defaults to 50.) reference impedance for the calculation
        @return boolean whether the device was created.
        @throw SignalIntegrityExceptionDeviceParser if the device cannot be created.
        """
        # pragma: silent exclude
        from SignalIntegrity.Lib.SParameters import SParameterFile
        from SignalIntegrity.Lib.Devices.CurrentAmplifier import CurrentAmplifier
        from SignalIntegrity.Lib.Devices.CurrentControlledCurrentSource import CurrentControlledCurrentSource
        from SignalIntegrity.Lib.Devices.CurrentControlledVoltageSource import CurrentControlledVoltageSource
        from SignalIntegrity.Lib.Devices.DirectionalCoupler import DirectionalCoupler
        from SignalIntegrity.Lib.Devices.Ground import Ground
        from SignalIntegrity.Lib.Devices.IdealTransformer import IdealTransformer
        from SignalIntegrity.Lib.Devices.MixedModeConverter import MixedModeConverter
        from SignalIntegrity.Lib.Devices.Open import Open
        from SignalIntegrity.Lib.Devices.OperationalAmplifier import OperationalAmplifier
        from SignalIntegrity.Lib.Devices.SeriesZ import SeriesZ
        from SignalIntegrity.Lib.Devices.TerminationZ import TerminationZ
        from SignalIntegrity.Lib.Devices.MixedModeConverter import MixedModeConverterVoltage
        from SignalIntegrity.Lib.Devices.Thru import Thru
        from SignalIntegrity.Lib.Devices.VoltageAmplifier import VoltageAmplifier
        from SignalIntegrity.Lib.Devices.ShuntZ import ShuntZ
        from SignalIntegrity.Lib.Devices.Tee import Tee
        from SignalIntegrity.Lib.Devices.TransconductanceAmplifier import TransconductanceAmplifier
        from SignalIntegrity.Lib.Devices.TransresistanceAmplifier import TransresistanceAmplifier
        from SignalIntegrity.Lib.Devices.VoltageControlledVoltageSource import VoltageControlledVoltageSource
        from SignalIntegrity.Lib.Devices.VoltageControlledCurrentSource import VoltageControlledCurrentSource
        from SignalIntegrity.Lib.Devices.IdealRelay import IdealRelay
        from SignalIntegrity.Lib.Fit.RLGCFitFromFile import RLGCFitFromFile
        from SignalIntegrity.Lib.SParameters.Devices.SeriesRse import SeriesRse
        from SignalIntegrity.Lib.SParameters.Devices.Mutual import Mutual
        from SignalIntegrity.Lib.SParameters.Devices.SeriesC import SeriesC
        from SignalIntegrity.Lib.SParameters.Devices.SeriesL import SeriesL
        from SignalIntegrity.Lib.SParameters.Devices.TerminationC import TerminationC
        from SignalIntegrity.Lib.SParameters.Devices.TerminationL import TerminationL
        from SignalIntegrity.Lib.SParameters.Devices.TLineLossless import TLineLossless
        from SignalIntegrity.Lib.SParameters.Devices.TLineLossy import TLineLossy
        from SignalIntegrity.Lib.SParameters.Devices.TLineTwoPortCOM import TLineTwoPortCOM
        from SignalIntegrity.Lib.SParameters.Devices.TLineTwoPortRLGC import TLineTwoPortRLGC
        from SignalIntegrity.Lib.Exception import SignalIntegrityExceptionDeviceParser
        from SignalIntegrity.Lib.Measurement.CalKit.Standards.ShortStandard import ShortStandard
        from SignalIntegrity.Lib.Measurement.CalKit.Standards.OpenStandard import OpenStandard
        from SignalIntegrity.Lib.Measurement.CalKit.Standards.LoadStandard import LoadStandard
        from SignalIntegrity.Lib.Measurement.CalKit.Standards.ThruStandard import ThruStandard
        from SignalIntegrity.Lib.Measurement.CalKit.Standards.Offset import Offset
        from SignalIntegrity.Lib.SParameters.Devices.TLineDifferentialRLGC import TLineDifferentialRLGC
        from SignalIntegrity.Lib.Measurement.Calibration.NetworkAnalyzer import NetworkAnalyzer
        from SignalIntegrity.Lib.SParameters.Devices.WElement import WElementFile
        from SignalIntegrity.Lib.SParameters.Devices.ClassicalFilter import ButterworthLowPassFilter,BesselLowPassFilter
        from SignalIntegrity.Lib.SParameters.Devices.Laplace import Laplace
        from SignalIntegrity.Lib.SParameters.Devices.Equalizer import FFE,CTLE
        from SignalIntegrity.Lib.SParameters.Devices.ImpulseResponseFilter import ImpulseResponseFilter
        from SignalIntegrity.Lib.SParameters.Devices.Parallel import Parallel
        # pragma: include
        self.dev=None
        if len(argsList) == 0:
            return False
        name=argsList[0].lower()
        argsList=argsList[1:]
        for device in self:
            if device.ports is not None:
                if isinstance(device.ports,int):
                    if device.ports != ports:
                        continue
                elif isinstance(device.ports,str):
                    if '-' in device.ports:
                        (minPort,maxPort) = device.ports.split('-')
                        if ports < int(minPort):
                            continue
                        if ports > int(maxPort):
                            continue
                    else:
                        acceptablePorts = device.ports.split(',')
                        if not any(ports == int(acceptablePort)
                                   for acceptablePort in acceptablePorts):
                            continue
            if device.devicename != name: continue
            # this is the device, try to make it
            if device.arginname:
                if len(argsList) > 0:
                    argsList=['']+argsList
            # pragma: silent exclude
            if len(argsList)//2*2 != len(argsList): # must be keyword value pairs
                raise SignalIntegrityExceptionDeviceParser(
                    'arguments must come in keyword pairs: '+name+' '+' '.join(argsList))
            # pragma: include
            argsProvidedDict = {argsList[i]:argsList[i+1]
                                for i in range(0,len(argsList),2)}
            # pragma: silent exclude
            extraArgs={}
            if not all(key in device.defaults for key in argsProvidedDict.keys()):
                invalidKeyList=[]
                for key in argsProvidedDict.keys():
                    if key not in device.defaults:
                        invalidKeyList.append(key)
                        extraArgs[key]=argsProvidedDict[key]
                if not '**extraArgs' in device.func:
                    raise SignalIntegrityExceptionDeviceParser(
                        'argument keyword(s) invalid: '+str(invalidKeyList)+' for '+name)
            # pragma: include
            arg=copy.copy(device.defaults)
            arg.update(argsProvidedDict)
            # pragma: silent exclude
            if not all(arg[key] != None for key in arg.keys()):
                argNotProvidedList=[]
                for key in arg:
                    if arg[key] == None:
                        argNotProvidedList.append(key)
                raise SignalIntegrityExceptionDeviceParser(
                    'mandatory keyword(s) not supplied: '+str(argNotProvidedList)+' for '+name)
            # pragma: include
            # pragma: silent exclude
            arg['z0']=Z0
            try:
            # pragma: include outdent
                self.dev=eval(device.func)
                self.frequencyDependent=device.frequencyDependent
            # pragma: silent exclude indent
            except:
                try:
                    f=[0]
                    eval(device.func)
                except:
                    raise SignalIntegrityExceptionDeviceParser(
                        'device '+name+' could not be instantiated with arguments: '+' '.join(argsList))
                raise SignalIntegrityExceptionDeviceParser(
                    'frequency dependent device '+name+' could not be instantiated because no frequencies provided')
            # pragma: include
            return True
        return False
    # pragma: silent exclude
    ##
    # @var dev
    # instance of class SParameters or list of list matrix when not frequency dependent.
    # @var frequencyDependent
    # boolean whether dev is frequency dependent.
    # pragma: include

class DeviceParser():
    """contains s-parameters of devices made from a netlist line"""
    deviceFactory=DeviceFactory()
    def __init__(self,f,ports,callback,argsList, Z0=50.):
        """Constructor
        makes a device from a set of arguments

        The device is assigned to self.m_spf if frequencyDependent and assumed
        to be an instance of class SParameters.
        Otherwise, it is assigned to self.m_sp and is assumed to be a list of
        list matrix.

        The intent of this class is that "Parser" classes use this DeviceParser
        to parse netlist lines that have 'device'
        as the first token.  It keeps these s-parameters and assigns them as
        it loops over the frequencies generating numeric
        solutions.

        @param f list of frequencies
        @param ports integer number of ports
        @param callback function pointer callback function (use None for no callback).
        @param argsList list of arguments.  The name of the device is the
        first argument.
        @param Z0 float (optional, defaults to 50.) reference impedance for the calculation
        If the device has no keyword for the argument, then that argument is next. 
        Otherwise, besides the name and the argument with no keyword, the
        remaining arguments come in keyword/value pairs where the
        keyword is a string and the value is the value of the keyword.  
        The callback function is used to pass down into s-parameter files that are actually
        SignalIntegrity projects so that progress can be tracked and the UI thread can be kept
        updated.
        @return None
        @throw SignalIntegrityExceptionDeviceParser if the device cannot be created.
        @see SignalIntegrity.Parsers.SystemDescriptionParser
        """
        # pragma: silent exclude
        from SignalIntegrity.Lib.Exception import SignalIntegrityExceptionDeviceParser
        from SignalIntegrity.Lib.SubCircuits.SubCircuit import SubCircuit
        # pragma: include
        self.m_f=f
        self.m_sp=None
        self.m_spf=None
        if argsList is None:
            return
        if len(argsList) == 0:
            return
        if argsList[0] == 'subcircuit':
            self.m_spf=SubCircuit(self.m_f,argsList[1],
            ' '.join([x if len(x.split())==1 else "\'"+x+"\'" for x in argsList[2:]]))
            return
        if self.deviceFactory.MakeDevice(ports, callback, argsList, f, Z0=Z0):
            if self.deviceFactory.frequencyDependent:
                self.m_spf=self.deviceFactory.dev
            else:
                self.m_sp=self.deviceFactory.dev
        else:
            #print 'device not found: '+' '.join(argsList)
            raise SignalIntegrityExceptionDeviceParser(
                'device not found: '+' '.join(argsList))
        return
    # pragma: silent exclude
    ##
    # @var m_sp
    # None if device is frequency dependent otherwise an instance of class SParameters
    # @var m_spf
    # None if device is not frequency dependent otherwise a list of list s-parameter matrix
    # @var m_f
    # list of frequencies
    # pragma: include
