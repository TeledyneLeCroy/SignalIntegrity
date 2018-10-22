"""
TransconductanceAmplifier.py
"""

# Copyright (c) 2018 Teledyne LeCroy, Inc.
# All rights reserved worldwide.
#
# This file is part of PySI.
#
# PySI is free software: You can redistribute it and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation, either version
# 3 of the License, or any later version.
#
# This program is distrbuted in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.
# If not, see <https://www.gnu.org/licenses/>

def TransconductanceAmplifier(P,G,Zi,Zo,Z0=50.):
    """TransconductanceAmplifier
    2-4 Port Transconductance Amplifiers
    @param P integer number of ports (2-4)
    @param G float transconductance gain
    @param Zi float or complex input impedance
    @param Zo float or complex output impedance
    @param Z0 (optional) float reference impedance (defaults to 50 Ohms)
    @return list of list s-parameter matrix for a transconductance amplifier
    @remark The transconductance amplifier can be two, three or four ports
    @see TransconductanceAmplifierFourPort
    @see TransconductanceAmplifierThreePort
    @see TransconductanceAmplifierTwoPort
    """
    if P==2:
        return TransconductanceAmplifierTwoPort(G,Zi,Zo,Z0=50.)
    elif P==3:
        return TransconductanceAmplifierThreePort(G,Zi,Zo,Z0=50.)
    elif P==4:
        return TransconductanceAmplifierFourPort(G,Zi,Zo,Z0=50.)

def TransconductanceAmplifierFourPort(G,Zi,Zo,Z0=50.):
    """TransconductanceAmplifierFourPort
    Four port transconductance amplifier
    @param G float transconductance gain
    @param Zi float or complex input impedance
    @param Zo float or complex output impedance
    @param Z0 (optional) float reference impedance (defaults to 50 Ohms)
    @return list of list s-parameter matrix for a transconductance amplifier
    @remark
    The voltage sense element senses the voltage with the plus terminal at port 1
    and and the minus terminal at port 2 shunted with impedance of Zi.\n
    The current generated by the amplifier enters port 4 and exits port 3 and
    is shunted with Zo.\n
    """
    S11=Zi/(Zi+2.*Z0)
    S12=2.*Z0/(Zi+2.*Z0)
    S13=0
    S14=0
    S21=S12
    S22=S11
    S23=0
    S24=0
    S31=2.*G*Zi*Zo*Z0/((Zi+2.*Z0)*(Zo+2.*Z0))
    S32=-S31
    S33=Zo/(Zo+2.*Z0)
    S34=2.*Z0/(Zo+2.*Z0)
    S41=S32
    S42=S31
    S43=S34
    S44=S33
    return [[S11,S12,S13,S14],
            [S21,S22,S23,S24],
            [S31,S32,S33,S34],
            [S41,S42,S43,S44]]

def TransconductanceAmplifierThreePort(G,Zi,Zo,Z0=50.):
    """TransconductanceAmplifierThreePort
    Three port transconductance amplifier
    @param G float transconductance gain
    @param Zi float or complex input impedance
    @param Zo float or complex output impedance
    @param Z0 (optional) float reference impedance (defaults to 50 Ohms)
    @return list of list s-parameter matrix for a transconductance amplifier.
    @remark
    The three port transconductance amplifier is the same as the four port transconductance amplifier with
    ports two and three connected together and exposed as a single port.\n
    The voltage sense element senses the voltage with the plus terminal at port 1
    and and the minus terminal at port 3 shunted with impedance of Zi.\n
    The current generated by the amplifier enters port 3 and exits port 2 and
    is shunted with Zo.\n
    """
    D=3.*Z0*Z0+(2.*Zo+2.*Zi-G*Zi*Zo)*Z0+Zo*Zi
    S11=(Zo*Zi+Z0*(2.*Zi-G*Zi*Zo)-Z0*Z0)/D
    S12=(2.*Z0*Z0)/D
    S13=(2.*Z0*Z0+2.*Zo*Z0)/D
    S21=(2.*Z0*Z0+2.*G*Zi*Zo*Z0)/D
    S22=(Zo*Zi+Z0*(2.*Zo-G*Zi*Zo)-Z0*Z0)/D
    S23=(2.*Z0*Z0+Z0*(2.*Zi-2.*G*Zi*Zo))/D
    S31=(2.*Z0*Z0+Z0*(2.*Zo-2.*G*Zi*Zo))/D
    S32=(2.*Z0*Z0+2.*Zi*Z0)/D
    S33=(Zo*Zi-Z0*Z0+G*Zi*Zo*Z0)/D
    return [[S11,S12,S13],
            [S21,S22,S23],
            [S31,S32,S33]]


def TransconductanceAmplifierTwoPort(G,Zi,Zo,Z0=50.):
    """TransconductanceAmplifierTwoPort
    Two port transconductance amplifier
    @param G float transconductance gain
    @param Zi float or complex input impedance
    @param Zo float or complex output impedance
    @param Z0 (optional) float reference impedance (defaults to 50 Ohms)
    @return list of list s-parameter matrix for a transconductance amplifier
    @remark
    The two port transconductance amplifier is the same as the three port transconductance amplifier with
    port 3 grounded.\n
    The voltage sense element senses the voltage  to ground at port 1 shunted to ground
    with impedance of Zi.\n
    The current generated by the amplifier exits port 2 and
    is shunted to ground with Zo.\n
    """
    return [[(Zi-Z0)/(Zi+Z0),0.],[2.*G*Zi*Zo*Z0/((Zi+Z0)*(Zo+Z0)),(Zo-Z0)/(Zo+Z0)]]