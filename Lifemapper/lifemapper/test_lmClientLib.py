"""
@summary: Test module for the Lifemapper client library
@author: CJ Grady
@organization: Lifemapper (http://lifemapper.org)
@version: 2.1.3
@status: release

@license: Copyright (C) 2014, University of Kansas Center for Research

          Lifemapper Project, lifemapper [at] ku [dot] edu, 
          Biodiversity Institute,
          1345 Jayhawk Boulevard, Lawrence, Kansas, 66045, USA
   
          This program is free software; you can redistribute it and/or modify 
          it under the terms of the GNU General Public License as published by 
          the Free Software Foundation; either version 2 of the License, or (at 
          your option) any later version.
  
          This program is distributed in the hope that it will be useful, but 
          WITHOUT ANY WARRANTY; without even the implied warranty of 
          MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU 
          General Public License for more details.
  
          You should have received a copy of the GNU General Public License 
          along with this program; if not, write to the Free Software 
          Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 
          02110-1301, USA.
"""
import logging
import unittest

import test_sdm
import test_rad

# .............................................................................
def getTestSuites():
   """
   @summary: Gets the test suites for the module
   @return: A list of test suites
   """
   testSuites = []
   testSuites.append(test_rad.getTestSuites())
   testSuites.append(test_sdm.getTestSuites())
   return testSuites

# ============================================================================
# = Main                                                                     =
# ============================================================================

if __name__ == '__main__':
   #tests
   logging.basicConfig(level = logging.DEBUG)

   for suite in getTestSuites():
      unittest.TextTestRunner(verbosity=2).run(suite)
