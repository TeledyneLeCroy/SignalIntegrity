"""
TestRoutineWriter.py
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
import unittest

from TestHelpers import *

class TestRoutineWriter(unittest.TestCase,RoutineWriterTesterHelper):
    def __init__(self, methodName='runTest'):
        RoutineWriterTesterHelper.__init__(self)
        unittest.TestCase.__init__(self,methodName)
    def testExampleCode(self):
        self.WriteCode('TestSystemDescription.py','testSystemDescriptionExampleBlock(self)',self.standardHeader)

if __name__ == '__main__':
    unittest.main()