"""
@summary: Tests for Lifemapper SDM web services
@author: CJ Grady
@version: 2.1.3
@status: release

@license: gpl2
@copyright: Copyright (C) 2014, University of Kansas Center for Research

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
from mx.DateTime import gmt
import os
import unittest

from lmClientLib import LMClient

UT_USER = "unitTest"
UT_PWD = "unitTest"

# .............................................................................
class TestSdmAlgorithmsAnon(unittest.TestCase):
   """
   @summary: Test class that tests SDM algorithms for an anonymous user
   """
   # .........................................
   def setUp(self):
      self.cl = LMClient()

   # .........................................
   def tearDown(self):
      self.cl.logout()

   # .........................................
   def test_algorithmsPresent(self):
      self.assertGreater(len(self.cl.sdm.algos), 0, "No algorithms present")
   
   # .........................................
   def test_checkParameters(self):
      code = "BIOCLIM"
      alg = self.cl.sdm.getAlgorithmFromCode(code)
      self.assertEqual(len(alg.parameters), 1)
   
   # .........................................
   def test_getATTMAXENT(self):
      code = "ATT_MAXENT"
      alg = self.cl.sdm.getAlgorithmFromCode(code)
      self.assertEqual(alg.code, code)
   
   # .........................................
   def test_getBIOCLIM(self):
      code = "BIOCLIM"
      alg = self.cl.sdm.getAlgorithmFromCode(code)
      self.assertEqual(alg.code, code)
   
   # .........................................
   def test_getGARPBS(self):
      code = "GARP_BS"
      alg = self.cl.sdm.getAlgorithmFromCode(code)
      self.assertEqual(alg.code, code)
   
   # .........................................
   def test_getInvalidAlgorithm(self):
      code = "INVALID_ALGORITHM"
      self.assertRaises(Exception, self.cl.sdm.getAlgorithmFromCode, code)
   
# .............................................................................
class TestSdmAlgorithmsUser(unittest.TestCase):
   """
   @summary: Test class that tests SDM algorithms for a logged in user
   """
   # .........................................
   def setUp(self):
      self.cl = LMClient(userId=UT_USER, pwd=UT_PWD)

   # .........................................
   def tearDown(self):
      self.cl.logout()

   # .........................................
   def test_algorithmsPresent(self):
      self.assertGreater(len(self.cl.sdm.algos), 0, "No algorithms present")
   
   # .........................................
   def test_checkParameters(self):
      code = "BIOCLIM"
      alg = self.cl.sdm.getAlgorithmFromCode(code)
      self.assertEqual(len(alg.parameters), 1)
   
   # .........................................
   def test_getATTMAXENT(self):
      code = "ATT_MAXENT"
      alg = self.cl.sdm.getAlgorithmFromCode(code)
      self.assertEqual(alg.code, code)
   
   # .........................................
   def test_getBIOCLIM(self):
      code = "BIOCLIM"
      alg = self.cl.sdm.getAlgorithmFromCode(code)
      self.assertEqual(alg.code, code)
   
   # .........................................
   def test_getGARPBS(self):
      code = "GARP_BS"
      alg = self.cl.sdm.getAlgorithmFromCode(code)
      self.assertEqual(alg.code, code)
   
   # .........................................
   def test_getInvalidAlgorithm(self):
      code = "INVALID_ALGORITHM"
      self.assertRaises(Exception, self.cl.sdm.getAlgorithmFromCode, code)
   
# .............................................................................
class TestSdmExperimentsAnon(unittest.TestCase):
   """
   @summary: Test class that tests SDM experiments for the anonymous user
   """
   # .........................................
   def setUp(self):
      self.cl = LMClient()

   # .........................................
   def tearDown(self):
      self.cl.logout()

   # .........................................
   def test_countNoParameters(self):
      self.cl.sdm.countExperiments()
   
   # .........................................
   def test_countWithParameters(self):
      self.cl.sdm.countExperiments(algorithmCode="BIOCLIM", public=True)
   
   # .........................................
   def test_countConflictingParameters(self):
      self.assertEqual(self.cl.sdm.countExperiments(afterTime="2012-10-15", 
                                                   beforeTime="2012-08-08"), 0)
   # .........................................
   def test_getExperimentValid(self):
      expId = self.cl.sdm.listExperiments(status=300)[0].id
      exp = self.cl.sdm.getExperiment(expId)
      self.assertEqual(str(exp.id), str(expId))
      
   # .........................................
   def test_getExperimentInvalid(self):
      self.assertRaises(Exception, self.cl.sdm.getExperiment, -12345678)
   
   # .........................................
   def test_listWithParameters(self):
      self.cl.sdm.listExperiments(algorithmCode='GARP_BS', page=1, perPage=3)
   
   # .........................................
   def test_listConflictingParameters(self):
      self.assertEqual(len(self.cl.sdm.listExperiments(afterTime="2012-10-15", 
                                                  beforeTime="2012-08-08")), 0)
   
   # .........................................
   def test_postInvalidAlgorithm(self):
      alg = None
      mdlScn = self.cl.sdm.listScenarios(public=True, perPage=1)[0].id
      occSet = self.cl.sdm.listOccurrenceSets(minimumNumberOfPoints=50, public=True, perPage=1)[0].id
      self.assertRaises(Exception, self.cl.sdm.postExperiment, alg, mdlScn, occSet)
   
   # .........................................
   def test_postInvalidModelingScenario(self):
      alg = self.cl.sdm.getAlgorithmFromCode('BIOCLIM')
      mdlScn = None
      occSet = self.cl.sdm.listOccurrenceSets(minimumNumberOfPoints=50, public=True, perPage=1)[0].id
      self.assertRaises(Exception, self.cl.sdm.postExperiment, alg, mdlScn, occSet)
   
   # .........................................
   def test_postInvalidOccurrenceSet(self):
      alg = self.cl.sdm.getAlgorithmFromCode('BIOCLIM')
      mdlScn = self.cl.sdm.listScenarios(public=True, perPage=1)[0].id
      occSet = None
      self.assertRaises(Exception, self.cl.sdm.postExperiment, alg, mdlScn, occSet)
   
   # .........................................
   def test_postValid(self):
      alg = self.cl.sdm.getAlgorithmFromCode('BIOCLIM')
      mdlScn = self.cl.sdm.listScenarios(public=True, perPage=1, epsgCode=4326)[0].id
      occSet = self.cl.sdm.listOccurrenceSets(minimumNumberOfPoints=50, public=True, epsgCode=4326, perPage=1)[0].id
      prjScns = [prj.id for prj in self.cl.sdm.listScenarios(matchingScenario=mdlScn, public=True)]
      self.cl.sdm.postExperiment(alg, mdlScn, occSet, prjScns=prjScns)
   
   # .........................................
   def test_postValidWithMask(self):
      alg = self.cl.sdm.getAlgorithmFromCode("GARP_BS")
      mdlMaskId = self.cl.sdm.listLayers(epsgCode=4326, public=True, perPage=1)[0].id
      mdlScn = self.cl.sdm.listScenarios(public=True, perPage=1, epsgCode=4326)[0].id
      occSet = self.cl.sdm.listOccurrenceSets(minimumNumberOfPoints=50, public=True, epsgCode=4326, perPage=1)[0].id
      prjScns = [prj.id for prj in self.cl.sdm.listScenarios(matchingScenario=mdlScn, public=True)]
      self.cl.sdm.postExperiment(alg, mdlScn, occSet, prjScns=prjScns, mdlMask=mdlMaskId, prjMask=mdlMaskId)
      
# .............................................................................
class TestSdmExperimentsUser(unittest.TestCase):
   """
   @summary: Test class that tests SDM experiments for an authenticated user
   """
   # .........................................
   def setUp(self):
      self.cl = LMClient(userId=UT_USER, pwd=UT_PWD)

   # .........................................
   def tearDown(self):
      self.cl.logout()

   # .........................................
   def test_countNoParameters(self):
      self.cl.sdm.countExperiments()
   
   # .........................................
   def test_countWithParameters(self):
      self.cl.sdm.countExperiments(algorithmCode="BIOCLIM", public=True)
   
   # .........................................
   def test_countConflictingParameters(self):
      self.assertEqual(self.cl.sdm.countExperiments(afterTime="2012-10-15", 
                                                   beforeTime="2012-08-08"), 0)
   
   # .........................................
   def test_countAllPublic(self):
      self.cl.sdm.countExperiments(public=True)
   
   # .........................................
   def test_countWithParametersPublic(self):
      self.cl.sdm.countExperiments(algorithmCode="GARP_BS", public=True)
   
   # .........................................
   def test_countConflictingParamsPublic(self):
      self.assertEqual(self.cl.sdm.countExperiments(afterTime="2012-10-15", 
                                                   beforeTime="2012-08-08",
                                                   public=True), 0)
   
   # .........................................
   def test_getExperimentValid(self):
      expId = self.cl.sdm.listExperiments(status=300)[0].id
      exp = self.cl.sdm.getExperiment(expId)
      self.assertEqual(str(exp.id), str(expId))
      
   # .........................................
   def test_getExperimentValidPublic(self):
      expId = self.cl.sdm.listExperiments(status=300, public=True)[0].id
      exp = self.cl.sdm.getExperiment(expId)
      self.assertEqual(str(exp.id), str(expId))

   # .........................................
   def test_getExperimentInvalid(self):
      self.assertRaises(Exception, self.cl.sdm.getExperiment, -12345678)
      
   # .........................................
   def test_listDefaults(self):
      self.cl.sdm.listExperiments()
   
   # .........................................
   def test_listWithParameters(self):
      self.cl.sdm.listExperiments(algorithmCode='GARP_BS', page=1, perPage=3)
   
   # .........................................
   def test_listConflictingParameters(self):
      self.assertEqual(len(self.cl.sdm.listExperiments(afterTime="2012-10-15", 
                                                  beforeTime="2012-08-08")), 0)
   
   # .........................................
   def test_listDefaultsPublic(self):
      self.cl.sdm.listExperiments(public=True)
   
   # .........................................
   def test_listWithParametersPublic(self):
      self.cl.sdm.listExperiments(algorithmCode='BIOCLIM', page=3, perPage=30)
   
   # .........................................
   def test_listConflictingParametersPublic(self):
      self.assertEqual(len(self.cl.sdm.listExperiments(afterTime="2012-10-15", 
                                                  beforeTime="2012-08-08",
                                                  public=True)), 0)
   
   # .........................................
   def test_postInvalidAlgorithm(self):
      alg = None
      mdlScn = self.cl.sdm.listScenarios(public=True, perPage=1)[0].id
      occSet = self.cl.sdm.listOccurrenceSets(minimumNumberOfPoints=50, public=True, perPage=1)[0].id
      self.assertRaises(Exception, self.cl.sdm.postExperiment, alg, mdlScn, occSet)
   
   # .........................................
   def test_postInvalidModelingScenario(self):
      alg = self.cl.sdm.getAlgorithmFromCode('BIOCLIM')
      mdlScn = None
      occSet = self.cl.sdm.listOccurrenceSets(minimumNumberOfPoints=50, public=True, perPage=1)[0].id
      self.assertRaises(Exception, self.cl.sdm.postExperiment, alg, mdlScn, occSet)
   
   # .........................................
   def test_postInvalidOccurrenceSet(self):
      alg = self.cl.sdm.getAlgorithmFromCode('BIOCLIM')
      mdlScn = self.cl.sdm.listScenarios(public=True, perPage=1)[0].id
      occSet = None
      self.assertRaises(Exception, self.cl.sdm.postExperiment, alg, mdlScn, occSet)
   
   # .........................................
   def test_postValid(self):
      alg = self.cl.sdm.getAlgorithmFromCode('BIOCLIM')
      mdlScn = self.cl.sdm.listScenarios(public=True, perPage=1, epsgCode=4326)[0].id
      occSet = self.cl.sdm.listOccurrenceSets(minimumNumberOfPoints=50, epsgCode=4326, public=True, perPage=1)[0].id
      prjScns = [prj.id for prj in self.cl.sdm.listScenarios(matchingScenario=mdlScn, public=True)]
      self.cl.sdm.postExperiment(alg, mdlScn, occSet, prjScns=prjScns)
      
   # .........................................
   def test_postValidWithMask(self):
      alg = self.cl.sdm.getAlgorithmFromCode("GARP_BS")
      mdlMaskId = self.cl.sdm.listLayers(epsgCode=4326, public=True, perPage=1)[0].id
      mdlScn = self.cl.sdm.listScenarios(public=True, perPage=1, epsgCode=4326)[0].id
      occSet = self.cl.sdm.listOccurrenceSets(minimumNumberOfPoints=50, public=True, epsgCode=4326, perPage=1)[0].id
      prjScns = [prj.id for prj in self.cl.sdm.listScenarios(matchingScenario=mdlScn, public=True)]
      self.cl.sdm.postExperiment(alg, mdlScn, occSet, prjScns=prjScns, mdlMask=mdlMaskId, prjMask=mdlMaskId)
      
# .............................................................................
class TestSdmLayersAnon(unittest.TestCase):
   """
   @summary: Test class that tests SDM layers for the anonymous user
   """
   # .........................................
   def setUp(self):
      self.cl = LMClient()

   # .........................................
   def tearDown(self):
      self.cl.logout()

   # .........................................
   def test_countConflictingParameters(self):
      self.assertEqual(self.cl.sdm.countLayers(afterTime="2010-03-03", 
                                                  beforeTime="2009-12-31"), 0)

   # .........................................
   def test_countNoParameters(self):
      self.cl.sdm.countLayers()

   # .........................................
   def test_countWithParameters(self):
      self.cl.sdm.countLayers(epsgCode=4326)

   # .........................................
   def test_getLayerInvalid(self):
      self.assertRaises(Exception, self.cl.sdm.getLayer, -123456)

   # .........................................
   def test_getLayerValid(self):
      lyrId = self.cl.sdm.listLayers()[0].id
      lyr = self.cl.sdm.getLayer(lyrId)
      self.assertEqual(str(lyr.id), str(lyrId))

   # .........................................
   def test_getLayerValidKML(self):
      lyrId = self.cl.sdm.listLayers()[0].id
      _ = self.cl.sdm.getLayerKML(lyrId)
   
   # .........................................
   def test_getLayerValidTiff(self):
      lyrId = self.cl.sdm.listLayers()[0].id
      _ = self.cl.sdm.getLayerTiff(lyrId)
   
   # .........................................
   def test_listConflictingParameters(self):
      self.assertEqual(len(self.cl.sdm.listLayers(afterTime="2010-03-03", 
                                               beforeTime="2009-12-31")), 0)

   # .........................................
   def test_listDefaults(self):
      self.cl.sdm.listLayers()

   # .........................................
   def test_listWithParameters(self):
      self.cl.sdm.listLayers(epsgCode=4326)

   # .........................................
   def test_postInvalid(self):
      self.assertRaises(Exception, 
                        self.cl.sdm.postLayer, None, None, None, None, None)

   # .........................................
   def test_postValidFromFile(self):
      name = 'utLyrFile%s' % str(gmt().mjd)
      epsgCode = 4326
      envLayerType = 'unitTest'
      units = 'dd'
      dataFormat = "GTiff"
      fn = os.path.join('..', 'sampleData', 'demoLayer.tif')
      self.cl.sdm.postLayer(name, epsgCode, envLayerType, units, dataFormat, fileName=fn)

   # .........................................
   def test_postValidFromString(self):
      name = 'utLyrStr%s' % str(gmt().mjd)
      epsgCode = 4326
      envLayerType = 'unitTest'
      units = 'dd'
      dataFormat = "GTiff"
      fn = os.path.join('..', 'sampleData', 'demoLayer.tif')
      cnt = open(fn).read()
      self.cl.sdm.postLayer(name, epsgCode, envLayerType, units, dataFormat, layerContent=cnt)

# .............................................................................
class TestSdmLayersUser(unittest.TestCase):
   """
   @summary: Test class that tests SDM layers for an authenticated user
   """
   # .........................................
   def setUp(self):
      self.cl = LMClient(userId=UT_USER, pwd=UT_PWD)

   # .........................................
   def tearDown(self):
      self.cl.logout()

   # .........................................
   def test_countAllPublic(self):
      self.cl.sdm.countLayers(public=True)

   # .........................................
   def test_countConflictingParameters(self):
      self.assertEqual(self.cl.sdm.countLayers(afterTime="2010-03-03", 
                                                  beforeTime="2009-12-31"), 0)

   # .........................................
   def test_countConflictingParametersPublic(self):
      self.assertEqual(self.cl.sdm.countLayers(afterTime="2010-03-03", 
                                               beforeTime="2009-12-31",
                                               public=True), 0)

   # .........................................
   def test_countNoParameters(self):
      self.cl.sdm.countLayers()

   # .........................................
   def test_countWithParameters(self):
      self.cl.sdm.countLayers(epsgCode=4326)

   # .........................................
   def test_countWithParametersPublic(self):
      self.cl.sdm.countLayers(epsgCode=4326, public=True)

   # .........................................
   def test_getLayerInvalid(self):
      self.assertRaises(Exception, self.cl.sdm.getLayer, -123456)

   # .........................................
   def test_getLayerValid(self):
      lyrId = self.cl.sdm.listLayers()[0].id
      lyr = self.cl.sdm.getLayer(lyrId)
      self.assertEqual(str(lyr.id), str(lyrId))

   # .........................................
   def test_getLayerValidPublic(self):
      lyrId = self.cl.sdm.listLayers(public=True)[0].id
      lyr = self.cl.sdm.getLayer(lyrId)
      self.assertEqual(str(lyr.id), str(lyrId))

   # .........................................
   def test_getLayerValidKML(self):
      lyrId = self.cl.sdm.listLayers()[0].id
      _ = self.cl.sdm.getLayerKML(lyrId)
   
   # .........................................
   def test_getLayerValidPublicKML(self):
      lyrId = self.cl.sdm.listLayers(public=True)[0].id
      _ = self.cl.sdm.getLayerKML(lyrId)
   
   # .........................................
   def test_getLayerValidTiff(self):
      lyrId = self.cl.sdm.listLayers()[0].id
      _ = self.cl.sdm.getLayerTiff(lyrId)
   
   # .........................................
   def test_getLayerValidPublicTiff(self):
      lyrId = self.cl.sdm.listLayers(public=True)[0].id
      _ = self.cl.sdm.getLayerTiff(lyrId)

   # .........................................
   def test_listConflictingParameters(self):
      self.assertEqual(len(self.cl.sdm.listLayers(afterTime="2010-03-03", 
                                               beforeTime="2009-12-31")), 0)

   # .........................................
   def test_listConflictingParametersPublic(self):
      self.assertEqual(len(self.cl.sdm.listLayers(afterTime="2010-03-03", 
                                               beforeTime="2009-12-31",
                                               public=True)), 0)

   # .........................................
   def test_listDefaults(self):
      self.cl.sdm.listLayers()

   # .........................................
   def test_listDefaultsPublic(self):
      self.cl.sdm.listLayers(public=True)

   # .........................................
   def test_listWithParameters(self):
      self.cl.sdm.listLayers(epsgCode=4326)

   # .........................................
   def test_listWithParametersPublic(self):
      self.cl.sdm.listLayers(typeCode='BIO1', public=True)

   # .........................................
   def test_postInvalid(self):
      self.assertRaises(Exception, 
                        self.cl.sdm.postLayer, None, None, None, None, None)

   # .........................................
   def test_postValidFromFile(self):
      name = 'utLyrFile%s' % str(gmt().mjd)
      epsgCode = 4326
      envLayerType = 'unitTest'
      units = 'dd'
      dataFormat = "GTiff"
      fn = os.path.join('..', 'sampleData', 'demoLayer.tif')
      self.cl.sdm.postLayer(name, epsgCode, envLayerType, units, dataFormat, fileName=fn)

   # .........................................
   def test_postValidFromString(self):
      name = 'utLyrStr%s' % str(gmt().mjd)
      epsgCode = 4326
      envLayerType = 'unitTest'
      units = 'dd'
      dataFormat = "GTiff"
      fn = os.path.join('..', 'sampleData', 'demoLayer.tif')
      cnt = open(fn).read()
      self.cl.sdm.postLayer(name, epsgCode, envLayerType, units, dataFormat, layerContent=cnt)

# .............................................................................
class TestSdmOccurrenceSetsAnon(unittest.TestCase):
   """
   @summary: Test class that tests SDM occurrence sets for the anonymous user
   """
   # .........................................
   def setUp(self):
      self.cl = LMClient()

   # .........................................
   def tearDown(self):
      self.cl.logout()

   # .........................................
   def test_countConflictingParameters(self):
      self.assertEqual(self.cl.sdm.countOccurrenceSets(afterTime="2010-03-03", 
                                                  beforeTime="2009-12-31"), 0)

   # .........................................
   def test_countNoParameters(self):
      self.cl.sdm.countOccurrenceSets()

   # .........................................
   def test_countWithParameters(self):
      self.cl.sdm.countOccurrenceSets(epsgCode=4326)

   # .........................................
   def test_getOccurrenceSetInvalid(self):
      self.assertRaises(Exception, self.cl.sdm.getOccurrenceSet, -123456)

   # .........................................
   def test_getOccurrenceSetValid(self):
      occId = self.cl.sdm.listOccurrenceSets()[0].id
      occ = self.cl.sdm.getOccurrenceSet(occId)
      self.assertEqual(str(occ.id), str(occId))

   # .........................................
   def test_getOccurrenceSetValidKML(self):
      occId = self.cl.sdm.listOccurrenceSets()[0].id
      _ = self.cl.sdm.getOccurrenceSetKML(occId)
   
   # .........................................
   def test_getOccurrenceSetValidShapefile(self):
      occId = self.cl.sdm.listOccurrenceSets()[0].id
      _ = self.cl.sdm.getOccurrenceSetShapefile(occId)
   
   # .........................................
   def test_listConflictingParameters(self):
      self.assertEqual(len(self.cl.sdm.listOccurrenceSets(
                                               afterTime="2010-03-03", 
                                               beforeTime="2009-12-31")), 0)

   # .........................................
   def test_listDefaults(self):
      self.cl.sdm.listOccurrenceSets()

   # .........................................
   def test_listWithParameters(self):
      self.cl.sdm.listOccurrenceSets(epsgCode=4326)

   # .........................................
   def test_postInvalid(self):
      self.assertRaises(Exception, self.cl.sdm.postOccurrenceSet, 'failTest', 'badType')

   # .........................................
   def test_postValidCsv(self):
      name = 'utCsv%s' % str(gmt().mjd)
      epsgCode = 4326
      fileType = 'CSV'
      fn = os.path.join('..', 'sampleData', 'exampleCSV.csv')
      self.cl.sdm.postOccurrenceSet(name, fileType, fn, epsgCode)

   # .........................................
   def test_postValidShapefile(self):
      name = 'utShp%s' % str(gmt().mjd)
      epsgCode = 4326
      fileType = 'shapefile'
      fn = os.path.join('..', 'sampleData', 'exampleShapefile.zip')
      self.cl.sdm.postOccurrenceSet(name, fileType, fn, epsgCode)

# .............................................................................
class TestSdmOccurrenceSetsUser(unittest.TestCase):
   """
   @summary: Test class that tests SDM occurrence sets for an authenticated user
   """
   # .........................................
   def setUp(self):
      self.cl = LMClient(userId=UT_USER, pwd=UT_PWD)

   # .........................................
   def tearDown(self):
      self.cl.logout()

   # .........................................
   def test_countAllPublic(self):
      self.cl.sdm.countOccurrenceSets(public=True)

   # .........................................
   def test_countConflictingParameters(self):
      self.assertEqual(self.cl.sdm.countOccurrenceSets(afterTime="2010-03-03", 
                                                  beforeTime="2009-12-31"), 0)

   # .........................................
   def test_countConflictingParametersPublic(self):
      self.assertEqual(self.cl.sdm.countOccurrenceSets(afterTime="2010-03-03", 
                                               beforeTime="2009-12-31",
                                               public=True), 0)

   # .........................................
   def test_countNoParameters(self):
      self.cl.sdm.countOccurrenceSets()

   # .........................................
   def test_countWithParameters(self):
      self.cl.sdm.countOccurrenceSets(epsgCode=4326)

   # .........................................
   def test_countWithParametersPublic(self):
      self.cl.sdm.countOccurrenceSets(epsgCode=4326, public=True)

   # .........................................
   def test_getOccurrenceSetInvalid(self):
      self.assertRaises(Exception, self.cl.sdm.getOccurrenceSet, -123456)

   # .........................................
   def test_getOccurrenceSetValid(self):
      occId = self.cl.sdm.listOccurrenceSets()[0].id
      occ = self.cl.sdm.getOccurrenceSet(occId)
      self.assertEqual(str(occ.id), str(occId))

   # .........................................
   def test_getOccurrenceSetValidPublic(self):
      occId = self.cl.sdm.listOccurrenceSets(public=True)[0].id
      occ = self.cl.sdm.getOccurrenceSet(occId)
      self.assertEqual(str(occ.id), str(occId))

   # .........................................
   def test_getOccurrenceSetValidKML(self):
      occId = self.cl.sdm.listOccurrenceSets()[0].id
      _ = self.cl.sdm.getOccurrenceSetKML(occId)
   
   # .........................................
   def test_getOccurrenceSetValidPublicKML(self):
      occId = self.cl.sdm.listOccurrenceSets(public=True)[0].id
      _ = self.cl.sdm.getOccurrenceSetKML(occId)

   # .........................................
   def test_getOccurrenceSetValidShapefile(self):
      occId = self.cl.sdm.listOccurrenceSets()[0].id
      _ = self.cl.sdm.getOccurrenceSetShapefile(occId)
   
   # .........................................
   def test_getOccurrenceSetValidPublicShapefile(self):
      occId = self.cl.sdm.listOccurrenceSets(public=True)[0].id
      _ = self.cl.sdm.getOccurrenceSetShapefile(occId)

   # .........................................
   def test_listConflictingParameters(self):
      self.assertEqual(len(self.cl.sdm.listOccurrenceSets(
                                               afterTime="2010-03-03", 
                                               beforeTime="2009-12-31")), 0)

   # .........................................
   def test_listConflictingParametersPublic(self):
      self.assertEqual(len(self.cl.sdm.listOccurrenceSets(
                                               afterTime="2010-03-03", 
                                               beforeTime="2009-12-31",
                                               public=True)), 0)

   # .........................................
   def test_listDefaults(self):
      self.cl.sdm.listOccurrenceSets()

   # .........................................
   def test_listDefaultsPublic(self):
      self.cl.sdm.listOccurrenceSets(public=True)

   # .........................................
   def test_listWithParameters(self):
      self.cl.sdm.listOccurrenceSets(epsgCode=4326)

   # .........................................
   def test_listWithParametersPublic(self):
      self.cl.sdm.listOccurrenceSets(epsgCode=4326, public=True)

   # .........................................
   def test_postInvalid(self):
      self.assertRaises(Exception, self.cl.sdm.postOccurrenceSet, 'failTest', 'badType')

   # .........................................
   def test_postValidCsv(self):
      name = 'utCsv%s' % str(gmt().mjd)
      epsgCode = 4326
      fileType = 'CSV'
      fn = os.path.join('..', 'sampleData', 'exampleCSV.csv')
      self.cl.sdm.postOccurrenceSet(name, fileType, fn, epsgCode)

   # .........................................
   def test_postValidShapefile(self):
      name = 'utShp%s' % str(gmt().mjd)
      epsgCode = 4326
      fileType = 'shapefile'
      fn = os.path.join('..', 'sampleData', 'exampleShapefile.zip')
      self.cl.sdm.postOccurrenceSet(name, fileType, fn, epsgCode)

# .............................................................................
class TestSdmProjectionsAnon(unittest.TestCase):
   """
   @summary: Test class that tests SDM projections for the anonymous user
   """
   # .........................................
   def setUp(self):
      self.cl = LMClient()

   # .........................................
   def tearDown(self):
      self.cl.logout()

   # .........................................
   def test_countConflictingParameters(self):
      self.assertEqual(self.cl.sdm.countProjections(afterTime="2010-03-03", 
                                                  beforeTime="2009-12-31"), 0)

   # .........................................
   def test_countNoParameters(self):
      self.cl.sdm.countProjections()

   # .........................................
   def test_countWithParameters(self):
      self.cl.sdm.countProjections(epsgCode=4326)

   # .........................................
   def test_getProjectionInvalid(self):
      self.assertRaises(Exception, self.cl.sdm.getProjection, -123456)

   # .........................................
   def test_getProjectionValid(self):
      prjId = self.cl.sdm.listProjections()[0].id
      prj = self.cl.sdm.getProjection(prjId)
      self.assertEqual(str(prj.id), str(prjId))

   # .........................................
   def test_getProjectionValidKML(self):
      prjId = self.cl.sdm.listProjections(status=300)[0].id
      _ = self.cl.sdm.getProjectionKML(prjId)
   
   # .........................................
   def test_getProjectionValidTiff(self):
      prjId = self.cl.sdm.listProjections(status=300)[0].id
      _ = self.cl.sdm.getProjectionTiff(prjId)
   
   # .........................................
   def test_listConflictingParameters(self):
      self.assertEqual(len(self.cl.sdm.listProjections(afterTime="2010-03-03", 
                                               beforeTime="2009-12-31")), 0)

   # .........................................
   def test_listDefaults(self):
      self.cl.sdm.listProjections()

   # .........................................
   def test_listWithParameters(self):
      self.cl.sdm.listProjections(epsgCode=4326)

# .............................................................................
class TestSdmProjectionsUser(unittest.TestCase):
   """
   @summary: Test class that tests SDM projections for an authenticated user
   """
   # .........................................
   def setUp(self):
      self.cl = LMClient(userId=UT_USER, pwd=UT_PWD)

   # .........................................
   def tearDown(self):
      self.cl.logout()

   # .........................................
   def test_countAllPublic(self):
      self.cl.sdm.countProjections(public=True)

   # .........................................
   def test_countConflictingParameters(self):
      self.assertEqual(self.cl.sdm.countProjections(afterTime="2010-03-03", 
                                                  beforeTime="2009-12-31"), 0)

   # .........................................
   def test_countConflictingParametersPublic(self):
      self.assertEqual(self.cl.sdm.countProjections(afterTime="2010-03-03", 
                                               beforeTime="2009-12-31",
                                               public=True), 0)

   # .........................................
   def test_countNoParameters(self):
      self.cl.sdm.countProjections()

   # .........................................
   def test_countWithParameters(self):
      self.cl.sdm.countProjections(epsgCode=4326)

   # .........................................
   def test_countWithParametersPublic(self):
      self.cl.sdm.countProjections(epsgCode=4326, status=300, public=True)

   # .........................................
   def test_getProjectionInvalid(self):
      self.assertRaises(Exception, self.cl.sdm.getProjection, -123456)

   # .........................................
   def test_getProjectionValid(self):
      prjId = self.cl.sdm.listProjections()[0].id
      prj = self.cl.sdm.getProjection(prjId)
      self.assertEqual(str(prj.id), str(prjId))

   # .........................................
   def test_getProjectionValidPublic(self):
      prjId = self.cl.sdm.listProjections(public=True)[0].id
      prj = self.cl.sdm.getProjection(prjId)
      self.assertEqual(str(prj.id), str(prjId))

   # .........................................
   def test_getProjectionValidKML(self):
      prjId = self.cl.sdm.listProjections(status=300)[0].id
      _ = self.cl.sdm.getProjectionKML(prjId)
   
   # .........................................
   def test_getProjectionValidPublicKML(self):
      prjId = self.cl.sdm.listProjections(status=300, public=True)[0].id
      _ = self.cl.sdm.getProjectionKML(prjId)

   # .........................................
   def test_getProjectionValidTiff(self):
      prjId = self.cl.sdm.listProjections(status=300)[0].id
      _ = self.cl.sdm.getProjectionTiff(prjId)
   
   # .........................................
   def test_getProjectionValidPublicTiff(self):
      prjId = self.cl.sdm.listProjections(status=300, public=True)[0].id
      _ = self.cl.sdm.getProjectionTiff(prjId)

   # .........................................
   def test_listConflictingParameters(self):
      self.assertEqual(len(self.cl.sdm.listProjections(afterTime="2010-03-03", 
                                               beforeTime="2009-12-31")), 0)

   # .........................................
   def test_listConflictingParametersPublic(self):
      self.assertEqual(len(self.cl.sdm.listProjections(afterTime="2010-03-03", 
                                               beforeTime="2009-12-31",
                                               public=True)), 0)

   # .........................................
   def test_listDefaults(self):
      self.cl.sdm.listProjections()

   # .........................................
   def test_listDefaultsPublic(self):
      self.cl.sdm.listProjections(public=True)

   # .........................................
   def test_listWithParameters(self):
      self.cl.sdm.listProjections(epsgCode=4326)

   # .........................................
   def test_listWithParametersPublic(self):
      self.cl.sdm.listProjections(status=300, public=True)

# .............................................................................
class TestSdmScenariosAnon(unittest.TestCase):
   """
   @summary: Test class that tests SDM scenarios for the anonymous user
   """
   # .........................................
   def setUp(self):
      self.cl = LMClient()

   # .........................................
   def tearDown(self):
      self.cl.logout()

   # .........................................
   def test_countConflictingParameters(self):
      self.assertEqual(self.cl.sdm.countScenarios(afterTime="2010-03-03", 
                                                  beforeTime="2009-12-31"), 0)

   # .........................................
   def test_countNoParameters(self):
      self.cl.sdm.countScenarios()

   # .........................................
   def test_countWithParameters(self):
      self.cl.sdm.countScenarios(epsgCode=4326)

   # .........................................
   def test_getScenarioInvalid(self):
      self.assertRaises(Exception, self.cl.sdm.getScenario, -123456)

   # .........................................
   def test_getScenarioValid(self):
      lyrId = self.cl.sdm.listScenarios()[0].id
      lyr = self.cl.sdm.getScenario(lyrId)
      self.assertEqual(str(lyr.id), str(lyrId))

   # .........................................
   def test_listConflictingParameters(self):
      self.assertEqual(len(self.cl.sdm.listScenarios(afterTime="2010-03-03", 
                                               beforeTime="2009-12-31")), 0)

   # .........................................
   def test_listDefaults(self):
      self.cl.sdm.listScenarios()

   # .........................................
   def test_listWithParameters(self):
      self.cl.sdm.listScenarios(epsgCode=4326)

   # .........................................
   def test_postInvalid(self):
      self.assertRaises(Exception, self.cl.sdm.postScenario, [], 'utInvalid', 0, 'dd')

   # .........................................
   def test_postValid(self):
      code = 'ut%s' % str(gmt().mjd)
      epsgCode = 4326
      layers = [lyr.id for lyr in self.cl.sdm.listLayers(epsgCode=epsgCode, perPage=5)]
      units = 'dd'
      self.cl.sdm.postScenario(layers, code, epsgCode, units, title="Unit test scn", keywords=['unittest'])

# .............................................................................
class TestSdmScenariosUser(unittest.TestCase):
   """
   @summary: Test class that tests SDM scenarios for an authenticated user
   """
   # .........................................
   def setUp(self):
      self.cl = LMClient(userId=UT_USER, pwd=UT_PWD)

   # .........................................
   def tearDown(self):
      self.cl.logout()

   # .........................................
   def test_countAllPublic(self):
      self.cl.sdm.countScenarios(public=True)

   # .........................................
   def test_countConflictingParameters(self):
      self.assertEqual(self.cl.sdm.countScenarios(afterTime="2010-03-03", 
                                                  beforeTime="2009-12-31"), 0)

   # .........................................
   def test_countConflictingParametersPublic(self):
      self.assertEqual(self.cl.sdm.countScenarios(afterTime="2010-03-03", 
                                               beforeTime="2009-12-31",
                                               public=True), 0)

   # .........................................
   def test_countNoParameters(self):
      self.cl.sdm.countScenarios()

   # .........................................
   def test_countWithParameters(self):
      self.cl.sdm.countScenarios(epsgCode=4326)

   # .........................................
   def test_countWithParametersPublic(self):
      self.cl.sdm.countScenarios(epsgCode=4326, keyword=['observed'], public=True)

   # .........................................
   def test_getScenarioInvalid(self):
      self.assertRaises(Exception, self.cl.sdm.getScenario, -123456)

   # .........................................
   def test_getScenarioValid(self):
      lyrId = self.cl.sdm.listScenarios()[0].id
      lyr = self.cl.sdm.getScenario(lyrId)
      self.assertEqual(str(lyr.id), str(lyrId))

   # .........................................
   def test_getScenarioValidPublic(self):
      lyrId = self.cl.sdm.listScenarios(public=True)[0].id
      lyr = self.cl.sdm.getScenario(lyrId)
      self.assertEqual(str(lyr.id), str(lyrId))

   # .........................................
   def test_listConflictingParameters(self):
      self.assertEqual(len(self.cl.sdm.listScenarios(afterTime="2010-03-03", 
                                               beforeTime="2009-12-31")), 0)

   # .........................................
   def test_listConflictingParametersPublic(self):
      self.assertEqual(len(self.cl.sdm.listScenarios(afterTime="2010-03-03", 
                                               beforeTime="2009-12-31",
                                               public=True)), 0)

   # .........................................
   def test_listDefaults(self):
      self.cl.sdm.listScenarios()

   # .........................................
   def test_listDefaultsPublic(self):
      self.cl.sdm.listScenarios(public=True)

   # .........................................
   def test_listWithParameters(self):
      self.cl.sdm.listScenarios(epsgCode=4326)

   # .........................................
   def test_listWithParametersPublic(self):
      self.cl.sdm.listScenarios(keyword=['observed'], public=True)

   # .........................................
   def test_postInvalid(self):
      self.assertRaises(Exception, self.cl.sdm.postScenario, [], 'utInvalid', 0, 'dd')

   # .........................................
   def test_postValid(self):
      code = 'ut%s' % str(gmt().mjd)
      epsgCode = 4326
      layers = [lyr.id for lyr in self.cl.sdm.listLayers(epsgCode=epsgCode, perPage=5)]
      units = 'dd'
      self.cl.sdm.postScenario(layers, code, epsgCode, units, title="Unit test scn", keywords=['unittest'])

# .............................................................................
class TestSdmTypeCodesAnon(unittest.TestCase):
   """
   @summary: Test class that tests SDM type codes for the anonymous user
   """
   # .........................................
   def setUp(self):
      self.cl = LMClient()

   # .........................................
   def tearDown(self):
      self.cl.logout()

   # .........................................
   def test_countConflictingParameters(self):
      self.assertEqual(self.cl.sdm.countTypeCodes(afterTime="2010-03-03", 
                                                  beforeTime="2009-12-31"), 0)

   # .........................................
   def test_countNoParameters(self):
      self.cl.sdm.countTypeCodes()

   # .........................................
   def test_countWithParameters(self):
      self.cl.sdm.countTypeCodes(afterTime="2013-01-01")

   # .........................................
   def test_getTypeCodeInvalid(self):
      self.assertRaises(Exception, self.cl.sdm.getTypeCode, -123456)

   # .........................................
   def test_getTypeCodeValid(self):
      lyrId = self.cl.sdm.listTypeCodes()[0].id
      lyr = self.cl.sdm.getTypeCode(lyrId)
      self.assertEqual(str(lyr.id), str(lyrId))

   # .........................................
   def test_listConflictingParameters(self):
      self.assertEqual(len(self.cl.sdm.listTypeCodes(afterTime="2010-03-03", 
                                               beforeTime="2009-12-31")), 0)

   # .........................................
   def test_listDefaults(self):
      self.cl.sdm.listTypeCodes()

   # .........................................
   def test_postValid(self):
      code = 'ut%s' % str(gmt().mjd)
      title = "Unit test type code: %s" % code
      description = "This is a unit test of the type code service"
      self.cl.sdm.postTypeCode(code, title=title, description=description)

# .............................................................................
class TestSdmTypeCodesUser(unittest.TestCase):
   """
   @summary: Test class that tests SDM type codes for an authenticated user
   """
   # .........................................
   def setUp(self):
      self.cl = LMClient(userId=UT_USER, pwd=UT_PWD)

   # .........................................
   def tearDown(self):
      self.cl.logout()

   # .........................................
   def test_countAllPublic(self):
      self.cl.sdm.countTypeCodes(public=True)

   # .........................................
   def test_countConflictingParameters(self):
      self.assertEqual(self.cl.sdm.countTypeCodes(afterTime="2010-03-03", 
                                                  beforeTime="2009-12-31"), 0)

   # .........................................
   def test_countConflictingParametersPublic(self):
      self.assertEqual(self.cl.sdm.countTypeCodes(afterTime="2010-03-03", 
                                               beforeTime="2009-12-31",
                                               public=True), 0)

   # .........................................
   def test_countNoParameters(self):
      self.cl.sdm.countTypeCodes()

   # .........................................
   def test_countWithParameters(self):
      self.cl.sdm.countTypeCodes(afterTime="2013-01-01")

   # .........................................
   def test_countWithParametersPublic(self):
      self.cl.sdm.countTypeCodes(beforeTime="2013-04-08", public=True)

   # .........................................
   def test_getTypeCodeInvalid(self):
      self.assertRaises(Exception, self.cl.sdm.getTypeCode, -123456)

   # .........................................
   def test_getTypeCodeValid(self):
      lyrId = self.cl.sdm.listTypeCodes()[0].id
      lyr = self.cl.sdm.getTypeCode(lyrId)
      self.assertEqual(str(lyr.id), str(lyrId))

   # .........................................
   def test_getTypeCodeValidPublic(self):
      lyrId = self.cl.sdm.listTypeCodes(public=True)[0].id
      lyr = self.cl.sdm.getTypeCode(lyrId)
      self.assertEqual(str(lyr.id), str(lyrId))

   # .........................................
   def test_listConflictingParameters(self):
      self.assertEqual(len(self.cl.sdm.listTypeCodes(afterTime="2010-03-03", 
                                               beforeTime="2009-12-31")), 0)

   # .........................................
   def test_listConflictingParametersPublic(self):
      self.assertEqual(len(self.cl.sdm.listTypeCodes(afterTime="2010-03-03", 
                                               beforeTime="2009-12-31",
                                               public=True)), 0)

   # .........................................
   def test_listDefaults(self):
      self.cl.sdm.listTypeCodes()

   # .........................................
   def test_listDefaultsPublic(self):
      self.cl.sdm.listTypeCodes(public=True)

   # .........................................
   def test_postValid(self):
      code = 'ut%s' % str(gmt().mjd)
      title = "Unit test type code: %s" % code
      description = "This is a unit test of the type code service"
      self.cl.sdm.postTypeCode(code, title=title, description=description)

# .............................................................................
class TestOtherAnon(unittest.TestCase):
   """
   @summary: Test class that tests other functions for the anonymous user
   """
   # .........................................
   def setUp(self):
      self.cl = LMClient()

   # .........................................
   def tearDown(self):
      self.cl.logout()
      
   # .........................................
   def test_getOgcEndpointLayer(self):
      lyrId = self.cl.sdm.listLayers(perPage=1)[0].id
      lyr = self.cl.sdm.getLayer(lyrId)
      self.cl.sdm.getOgcEndpoint(lyr)

   # .........................................
   def test_getOgcEndpointOccurrenceSet(self):
      occId = self.cl.sdm.listOccurrenceSets(perPage=1)[0].id
      occ = self.cl.sdm.getOccurrenceSet(occId)
      self.cl.sdm.getOgcEndpoint(occ)

   # .........................................
   def test_getOgcEndpointProjection(self):
      prjId = self.cl.sdm.listProjections(perPage=1, status=300)[0].id
      prj = self.cl.sdm.getProjection(prjId)
      self.cl.sdm.getOgcEndpoint(prj)

   # .........................................
   def test_hintValid(self):
      self.assertLessEqual(len(self.cl.sdm.hint('acacia', maxReturned=3)), 3)

   # .........................................
   def test_hintNotEnoughChars(self):
      self.assertRaises(Exception, self.cl.sdm.hint, 'ly')

# .............................................................................
class TestOtherUser(unittest.TestCase):
   """
   @summary: Test class that tests other functions for an authenticated user
   """
   # .........................................
   def setUp(self):
      self.cl = LMClient(userId=UT_USER, pwd=UT_PWD)

   # .........................................
   def tearDown(self):
      self.cl.logout()
      
   # .........................................
   def test_getOgcEndpointLayer(self):
      lyrId = self.cl.sdm.listLayers(perPage=1)[0].id
      lyr = self.cl.sdm.getLayer(lyrId)
      self.cl.sdm.getOgcEndpoint(lyr)

   # .........................................
   def test_getOgcEndpointOccurrenceSet(self):
      occId = self.cl.sdm.listOccurrenceSets(perPage=1)[0].id
      occ = self.cl.sdm.getOccurrenceSet(occId)
      self.cl.sdm.getOgcEndpoint(occ)

   # .........................................
   def test_getOgcEndpointProjection(self):
      prjId = self.cl.sdm.listProjections(perPage=1, status=300)[0].id
      prj = self.cl.sdm.getProjection(prjId)
      self.cl.sdm.getOgcEndpoint(prj)

   # .........................................
   def test_getOgcEndpointLayerPublic(self):
      lyrId = self.cl.sdm.listLayers(perPage=1, public=True)[0].id
      lyr = self.cl.sdm.getLayer(lyrId)
      self.cl.sdm.getOgcEndpoint(lyr)

   # .........................................
   def test_getOgcEndpointOccurrenceSetPublic(self):
      occId = self.cl.sdm.listOccurrenceSets(perPage=1, public=True)[0].id
      occ = self.cl.sdm.getOccurrenceSet(occId)
      self.cl.sdm.getOgcEndpoint(occ)

   # .........................................
   def test_getOgcEndpointProjectionPublic(self):
      prjId = self.cl.sdm.listProjections(perPage=1, status=300, public=True)[0].id
      prj = self.cl.sdm.getProjection(prjId)
      self.cl.sdm.getOgcEndpoint(prj)
      
   # .........................................
   def test_hintValid(self):
      self.assertLessEqual(len(self.cl.sdm.hint('acacia', maxReturned=3)), 3)

   # .........................................
   def test_hintNotEnoughChars(self):
      self.assertRaises(Exception, self.cl.sdm.hint, 'ly')

# .............................................................................
def getTestSuites():
   """
   @summary: Gets the test suites for the module
   @return: A list of test suites
   """
   testSuites = []
   loader = unittest.TestLoader()
   testSuites.append(loader.loadTestsFromTestCase(TestSdmAlgorithmsAnon))
   testSuites.append(loader.loadTestsFromTestCase(TestSdmAlgorithmsUser))
   testSuites.append(loader.loadTestsFromTestCase(TestSdmExperimentsAnon))
   testSuites.append(loader.loadTestsFromTestCase(TestSdmExperimentsUser))
   testSuites.append(loader.loadTestsFromTestCase(TestSdmLayersAnon))
   testSuites.append(loader.loadTestsFromTestCase(TestSdmLayersUser))
   testSuites.append(loader.loadTestsFromTestCase(TestSdmOccurrenceSetsAnon))
   testSuites.append(loader.loadTestsFromTestCase(TestSdmOccurrenceSetsUser))
   testSuites.append(loader.loadTestsFromTestCase(TestSdmProjectionsAnon))
   testSuites.append(loader.loadTestsFromTestCase(TestSdmProjectionsUser))
   testSuites.append(loader.loadTestsFromTestCase(TestSdmScenariosAnon))
   testSuites.append(loader.loadTestsFromTestCase(TestSdmScenariosUser))
   testSuites.append(loader.loadTestsFromTestCase(TestSdmTypeCodesAnon))
   testSuites.append(loader.loadTestsFromTestCase(TestSdmTypeCodesUser))
   testSuites.append(loader.loadTestsFromTestCase(TestOtherAnon))
   testSuites.append(loader.loadTestsFromTestCase(TestOtherUser))
   return testSuites

# ============================================================================
# = Main                                                                     =
# ============================================================================

if __name__ == '__main__':
   #tests
#    logging.basicConfig(level = logging.DEBUG)
# 
#    for suite in getTestSuites():
#       unittest.TextTestRunner(verbosity=2).run(suite)
      
   unittest.main()
