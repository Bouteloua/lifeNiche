"""
@summary: Tests for Lifemapper RAD web services
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
from tempfile import mkstemp
from time import sleep
import unittest

from constants import JobStage
from lmClientLib import LMClient

UT_USER = "unitTest"
UT_PWD = "unitTest"

# .............................................................................
class TestRADBuckets(unittest.TestCase):
   """
   @summary: Test class that tests RAD buckets for an authenticated user
   """
   # .........................................
   def setUp(self):
      self.cl = LMClient(userId=UT_USER, pwd=UT_PWD)

   # .........................................
   def tearDown(self):
      self.cl.logout()

   # .........................................
   def test_countConflictingParameters(self):
      expId = self.cl.rad.listExperiments()[0].id
      self.assertEqual(self.cl.rad.countBuckets(expId, afterTime="2010-03-03", 
                                                  beforeTime="2009-12-31"), 0)

   # .........................................
   def test_countNoParameters(self):
      expId = self.cl.rad.listExperiments()[0].id
      self.cl.rad.countBuckets(expId)

   # .........................................
   def test_countWithInvalidExperiment(self):
      self.cl.rad.countBuckets(-12345)

   # .........................................
   def test_getBucketInvalid(self):
      expId = self.cl.rad.listExperiments()[0].id
      self.assertRaises(Exception, self.cl.rad.getBucket, expId, -123456)

   # .........................................
   def test_getBucketValid(self):
      expId = self.cl.rad.listExperiments()[0].id
      bktId = self.cl.rad.listBuckets(expId)[0].id
      bkt = self.cl.rad.getBucket(expId, bktId)
      self.assertEqual(str(bkt.id), str(bktId))

   # .........................................
   def test_listConflictingParameters(self):
      expId = self.cl.rad.listExperiments()[0].id
      self.assertEqual(len(self.cl.rad.listBuckets(expId, 
                                                   afterTime="2010-03-03", 
                                               beforeTime="2009-12-31")), 0)

   # .........................................
   def test_listDefaults(self):
      expId = self.cl.rad.listExperiments()[0].id
      self.cl.rad.listBuckets(expId)

   # .........................................
   def test_postInvalid(self):
      self.assertRaises(Exception, 
                        self.cl.rad.addBucket, None, filename=None)

   # .........................................
   def test_addBucket(self):
      epsgCode = 4326
      expId = self.cl.rad.listExperiments(epsgCode=epsgCode, perPage=1)[0].id
      shpName = "utNC%s" % str(gmt().mjd)
      cellShape = "square"
      cellSize = "2.5"
      mapUnits = "dd"
      bbox = "-50,0,-30,40"

      _ = self.cl.rad.addBucket(expId, shpName, cellShape, cellSize, mapUnits, 
                                                               epsgCode, bbox)

   # .........................................
   def test_getBucketShapegridDataInvalid(self):
      self.assertRaises(Exception, self.cl.rad.getBucketShapegridData, None, 123456, 
                        -12345)
    
   # .........................................
   def test_getBucketShapegridDataValid(self):
      expId = self.cl.rad.listExperiments()[0].id
      bktId = self.cl.rad.listBuckets(expId)[0].id
      fn = mkstemp()[1]
      self.cl.rad.getBucketShapegridData(fn, expId, bktId, intersected=False)
      os.remove(fn)

   # .........................................
   def test_getBucketShapegridDataValidIntersected(self):
      expId = self.cl.rad.listExperiments()[0].id
      bktId = self.cl.rad.listBuckets(expId)[0].id
      fn = mkstemp()[1]
      self.cl.rad.getBucketShapegridData(fn, expId, bktId, intersected=False)
      os.remove(fn)

   # .........................................
   def test_intersectBucket(self):
      expId, bktId = getNewExpBkt(self.cl)
      self.cl.rad.intersectBucket(expId, bktId)
   
   # .........................................
   def test_randomizeBucketSplotch(self):
      expId, bktId = getNewExpBkt(self.cl)
      self.cl.rad.randomizeBucket(expId, bktId, method='splotch')
   
   # .........................................
   def test_randomizeBucketSwap(self):
      expId, bktId = getNewExpBkt(self.cl)
      self.cl.rad.intersectBucket(expId, bktId)
      self.cl.rad.randomizeBucket(expId, bktId, method='swap')
   
# .............................................................................
class TestRADExperiments(unittest.TestCase):
   """
   @summary: Test class that tests RAD experiments for an authenticated user
   """
   # .........................................
   def setUp(self):
      self.cl = LMClient(userId=UT_USER, pwd=UT_PWD)

   # .........................................
   def tearDown(self):
      self.cl.logout()

   # .........................................
   def test_countConflictingParameters(self):
      self.assertEqual(self.cl.rad.countExperiments(afterTime="2010-03-03", 
                                                  beforeTime="2009-12-31"), 0)

   # .........................................
   def test_countNoParameters(self):
      self.cl.rad.countExperiments()

   # .........................................
   def test_countWithParameters(self):
      self.cl.rad.countExperiments(epsgCode=4326)
      
   # .........................................
   def test_getExperiment(self):
      expId = self.cl.rad.listExperiments(perPage=1)[0].id
      _ = self.cl.rad.getExperiment(expId)
   
   # .........................................
   def test_getExperimentInvalid(self):
      self.assertRaises(Exception, self.cl.rad.getExperiment, -12334)

   # .........................................
   def test_listConflictingParameters(self):
      self.assertEqual(len(self.cl.rad.listExperiments(afterTime="2010-03-03", 
                                               beforeTime="2009-12-31")), 0)

   # .........................................
   def test_listDefaults(self):
      self.cl.rad.listExperiments()

   # .........................................
   def test_listWithParameters(self):
      self.cl.rad.listExperiments(epsgCode=4326)

   # .........................................
   def test_postInvalid(self):
      self.assertRaises(Exception, self.cl.rad.postExperiment, None, None)
   
   # .........................................
   def test_postValid(self):
      name = "ut%s" % str(gmt().mjd)
      epsgCode = 4326
      self.cl.rad.postExperiment(name, epsgCode)
   
# .............................................................................
class TestRADLayers(unittest.TestCase):
   """
   @summary: Test class that tests RAD layers for an authenticated user
   """
   # .........................................
   def setUp(self):
      self.cl = LMClient(userId=UT_USER, pwd=UT_PWD)

   # .........................................
   def tearDown(self):
      self.cl.logout()

   # .........................................
   def test_countConflictingParameters(self):
      self.assertEqual(self.cl.rad.countLayers(afterTime="2010-03-03", 
                                                  beforeTime="2009-12-31"), 0)

   # .........................................
   def test_countNoParameters(self):
      self.cl.rad.countLayers()

   # .........................................
   def test_countWithParameters(self):
      self.cl.rad.countLayers(epsgCode=4326)

   # .........................................
   def test_getLayerInvalid(self):
      self.assertRaises(Exception, self.cl.rad.getLayer, -123456)

   # .........................................
   def test_getLayerValid(self):
      lyrId = self.cl.rad.listLayers()[0].id
      lyr = self.cl.rad.getLayer(lyrId)
      self.assertEqual(str(lyr.id), str(lyrId))

   # .........................................
   def test_listConflictingParameters(self):
      self.assertEqual(len(self.cl.rad.listLayers(afterTime="2010-03-03", 
                                               beforeTime="2009-12-31")), 0)

   # .........................................
   def test_listDefaults(self):
      self.cl.rad.listLayers()

   # .........................................
   def test_listWithParameters(self):
      self.cl.rad.listLayers(epsgCode=4326)

   # .........................................
   def test_postInvalid(self):
      self.assertRaises(Exception, 
                        self.cl.rad.postRaster, None, filename=None)

   # .........................................
   def test_postValidRasterFromFile(self):
      name = 'utLyrRstFile%s' % str(gmt().mjd)
      epsgCode = 4326
      fn = os.path.join('..', 'sampleData', 'demoLayer.tif')
      self.cl.rad.postRaster(name, epsgCode=epsgCode, filename=fn)

   # .........................................
   def test_postValidRasterFromString(self):
      name = 'utLyrRstStr%s' % str(gmt().mjd)
      epsgCode = 4326
      fn = os.path.join('..', 'sampleData', 'demoLayer.tif')
      cnt = open(fn).read()
      self.cl.rad.postRaster(name, epsgCode=epsgCode, layerContent=cnt)

   # .........................................
   def test_postValidVectorFromFileShapefile(self):
      name = 'utLyrVecShp%s' % str(gmt().mjd)
      fn = os.path.join('..', 'sampleData', 'radData', 'Accipiter_brachyurus.shp')
      self.cl.rad.postVector(name, filename=fn)
 
   # .........................................
   def test_postValidVectorFromFileZip(self):
      name = 'utLyrVecZip%s' % str(gmt().mjd)
      fn = os.path.join('..', 'sampleData', 'radData', 'Accipiter_brachyurus.zip')
      self.cl.rad.postVector(name, filename=fn)
 
   # .........................................
   def test_postValidVectorFromString(self):
      name = 'utLyrVec%s' % str(gmt().mjd)
      fn = os.path.join('..', 'sampleData', 'radData', 'Accipiter_brachyurus.zip')
      cnt = open(fn).read()
      self.cl.rad.postVector(name, layerContent=cnt)

# .............................................................................
class TestRADExpPALayers(unittest.TestCase):
   """
   @summary: Test class that tests presence / absence layers for an experiment
   """
   # .........................................
   def setUp(self):
      self.cl = LMClient(userId=UT_USER, pwd=UT_PWD)

   # .........................................
   def tearDown(self):
      self.cl.logout()

   # .........................................
   def test_addPALayer(self):
      expName = "utExpBktpalyr%s" % str(gmt().mjd)
      epsgCode = 4326
      # Create experiment
      exp = self.cl.rad.postExperiment(expName, epsgCode)
      lyr1 = self.cl.rad.postRaster('utRst1%s' % str(gmt().mjd), epsgCode=epsgCode, 
               filename=os.path.join('..', 'sampleData', 'demoLayer.tif'))
      lyr2 = self.cl.rad.postVector('utVec1%s' % str(gmt().mjd),
               filename=os.path.join('..', 'sampleData', 'radData', 
                                     'Accipiter_brachyurus.shp'))
      # Add layers
      self.cl.rad.addPALayer(exp.id, lyr1.id, 'pixel', 120, 254, 30)
      self.cl.rad.addPALayer(exp.id, lyr2.id, 'PRESENCE', 1, 2, 30)
   
   # .........................................
   def test_getPALayers(self):
      expId = self.cl.rad.listExperiments(perPage=1)[0].id
      self.cl.rad.getPALayers(expId)

# # .............................................................................
# class TestRADExpAncillaryLayers(unittest.TestCase):
#    """
#    @summary: Test class that tests ancillary layers for an experiment
#    """
#    # .........................................
#    def setUp(self):
#       self.cl = LMClient(userId=UT_USER, pwd=UT_PWD)
# 
#    # .........................................
#    def tearDown(self):
#       self.cl.logout()
# 
#    # .........................................
#    def test_addAncLayer(self):
#       expName = "utExpBktAnclyr%s" % str(gmt().mjd)
#       epsgCode = 4326
#       # Create experiment
#       exp = self.cl.rad.postExperiment(expName, epsgCode)
#       lyr1 = self.cl.rad.postRaster('utRst1%s' % str(gmt().mjd), epsgCode=epsgCode, 
#                filename=os.path.join('..', 'sampleData', 'demoLayer.tif'))
#       lyr2 = self.cl.rad.postVector('utVec1%s' % str(gmt().mjd),
#                filename=os.path.join('..', 'sampleData', 'radData', 
#                                      'Accipiter_brachyurus.shp'))
#       # Add layers
#       self.cl.rad.addAncLayer(exp.id, lyr1.id, attrValue='pixel', minPercent=30)
#       self.cl.rad.addAncLayer(exp.id, lyr2.id, attrValue='PRESENCE', minPercent=30)
#    
#    # .........................................
#    def test_getAncLayers(self):
#       expId = self.cl.rad.listExperiments(perPage=1)[0].id
#       self.cl.rad.getAncLayers(expId)

# .............................................................................
class TestRADPamSums(unittest.TestCase):
   """
   @summary: Test class that tests RAD pamsums for an authenticated user
   """
   # .........................................
   def setUp(self):
      self.cl = LMClient(userId=UT_USER, pwd=UT_PWD)

   # .........................................
   def tearDown(self):
      self.cl.logout()

   # .........................................
   def test_countConflictingParameters(self):
      expId, bktId = getNewExpBktWithPamsums(self.cl)
      self.assertEqual(self.cl.rad.countPamSums(expId, bktId, 
                                                afterTime="2010-03-03", 
                                                beforeTime="2009-12-31"), 0)

   # .........................................
   def test_countNoParameters(self):
      expId, bktId = getNewExpBktWithPamsums(self.cl)
      self.cl.rad.countPamSums(expId, bktId)

   # .........................................
   def test_countWithInvalidExperiment(self):
      self.cl.rad.countPamSums(-12345, 123)

   # .........................................
   def test_getPamSumInvalid(self):
      expId, bktId = getNewExpBktWithPamsums(self.cl)
      self.assertRaises(Exception, self.cl.rad.getPamSum, expId, bktId, -123456)

   # .........................................
   def test_getPamSumValid(self):
      expId, bktId = getNewExpBktWithPamsums(self.cl)
      psId = self.cl.rad.listPamSums(expId, bktId, perPage=1)[0].id
      ps = self.cl.rad.getPamSum(expId, bktId, psId)
      self.assertEqual(str(ps.id), str(psId))

   # .........................................
   def test_listConflictingParameters(self):
      expId, bktId = getNewExpBktWithPamsums(self.cl)
      self.assertEqual(len(self.cl.rad.listPamSums(expId, bktId, 
                                                   afterTime="2010-03-03", 
                                               beforeTime="2009-12-31")), 0)

   # .........................................
   def test_listDefaults(self):
      expId, bktId = getNewExpBktWithPamsums(self.cl)
      self.cl.rad.listPamSums(expId, bktId)

   # .........................................
   def test_getPamSumShapegrid(self):
      expId, bktId = getNewExpBktWithPamsums(self.cl)
      psId = self.cl.rad.listPamSums(expId, bktId, perPage=1, randomized=1, 
                                                          randomMethod=1)[0].id
#      self.cl.rad.calculatePamSumStatistics(expId, bktId, pamsumId=psId)
      print "Exp: %s, Bucket: %s, PamSum: %s" % (expId, bktId, psId)
      t = 0
      ps = self.cl.rad.getPamSum(expId, bktId, psId)
      status, stage = self.cl.rad.getStatusStage(ps)
      while stage != JobStage.CALCULATE and t < 601:
         t = t + 30
         sleep(30)
         ps = self.cl.rad.getPamSum(expId, bktId, psId)
         status, stage = self.cl.rad.getStatusStage(ps)
      if t >= 601:
         self.fail("Took too long to calculate statistics for pam sum")
      fn = mkstemp()[1]
      self.cl.rad.getPamSumShapegrid(fn, expId, bktId, "original")
      os.remove(fn)
   
   # .........................................
   def test_getPamSumStatistic(self):
      """
      @summary: Gets the available statistics for a pamsum
      @param expId: The id of the RAD experiment
      @param bucketId: The id of the RAD bucket
      @param pamSumId: The id of the pamsum to get statistics for
      @param stat: The key of the statistic to return
      """
      expId, bktId = getNewExpBktWithPamsums(self.cl)
      psId = self.cl.rad.listPamSums(expId, bktId, perPage=1, randomized=1, 
                                                          randomMethod=1)[0].id
#      self.cl.rad.calculatePamSumStatistics(expId, bktId, pamsumId=psId)
      print "Exp: %s, Bucket: %s, PamSum: %s" % (expId, bktId, psId)
      t = 0
      ps = self.cl.rad.getPamSum(expId, bktId, psId)
      status, stage = self.cl.rad.getStatusStage(ps)
      while status != 300 and t < 601:
         t = t + 30
         sleep(30)
         ps = self.cl.rad.getPamSum(expId, bktId, psId)
         status, stage = self.cl.rad.getStatusStage(ps)
      if t >= 601:
         self.fail("Took too long to calculate statistics for pam sum")
      ks = self.cl.rad.getPamSumStatisticsKeys(expId, bktId, psId)
      stat = self.cl.rad.getPamSumStatistic(expId, bktId, psId, ks[0])

   # .........................................
   def test_getPamSumStatisticsKeys(self):
      """
      @summary: Gets the available statistics for a pamsum
      @param expId: The id of the RAD experiment
      @param bucketId: The id of the RAD bucket
      @param pamSumId: The id of the pamsum to get statistics for
      @param keys: (optional) The type of keys to return
                               (keys | specieskeys | siteskeys | diversitykeys)
      """
      expId, bktId = getNewExpBktWithPamsums(self.cl)
      psId = self.cl.rad.listPamSums(expId, bktId, perPage=1, randomized=1, 
                                                         randomMethod=1)[0].id
#      self.cl.rad.calculatePamSumStatistics(expId, bktId, pamsumId=psId)
      t = 0
      print "Exp: %s, Bucket: %s, PamSum: %s" % (expId, bktId, psId)
      ps = self.cl.rad.getPamSum(expId, bktId, psId)
      status, stage = self.cl.rad.getStatusStage(ps)
      while status != 300 and t < 601:
         t = t + 30
         sleep(30)
         ps = self.cl.rad.getPamSum(expId, bktId, psId)
         status, stage = self.cl.rad.getStatusStage(ps)
      if t >= 601:
         self.fail("Took too long to calculate statistics for pam sum")
      _ = self.cl.rad.getPamSumStatisticsKeys(expId, bktId, psId)

#    # .........................................
#    def test_calculatePamSumStatistics(self):
#       expId, bktId = getNewExpBktWithPamsums(self.cl)
#       psId = self.cl.rad.listPamSums(expId, bktId, perPage=1)[0].id
#       self.cl.rad.calculatePamSumStatistics(expId, bktId, psId)

#    # .........................................
#    def test_compressPamSum(self):
#       expId, bktId = getNewExpBktWithPamsums(self.cl)
#       psId = self.cl.rad.listPamSums(expId, bktId, perPage=1, randomized=1, 
#                                                          randomMethod=2)[0].id
#       self.cl.rad.compressPamSum(expId, bktId, psId)
#    
# .............................................................................
class TestRADShapegrids(unittest.TestCase):
   """
   @summary: Test class that tests RAD shapegrids for an authenticated user
   """
   # .........................................
   def setUp(self):
      self.cl = LMClient(userId=UT_USER, pwd=UT_PWD)

   # .........................................
   def tearDown(self):
      self.cl.logout()

   # .........................................
   def test_countConflictingParameters(self):
      self.assertEqual(self.cl.rad.countShapegrids(afterTime="2010-03-03", 
                                                  beforeTime="2009-12-31"), 0)

   # .........................................
   def test_countNoParameters(self):
      self.cl.rad.countShapegrids()

   # .........................................
   def test_countWithParameters(self):
      self.cl.rad.countShapegrids(cellSides=4)

   # .........................................
   def test_getShapegridInvalid(self):
      self.assertRaises(Exception, self.cl.rad.getShapegrid, -123456)

   # .........................................
   def test_getShapegridValid(self):
      lyrId = self.cl.rad.listShapegrids()[0].id
      lyr = self.cl.rad.getShapegrid(lyrId)
      self.assertEqual(str(lyr.id), str(lyrId))

   # .........................................
   def test_listConflictingParameters(self):
      self.assertEqual(len(self.cl.rad.listShapegrids(afterTime="2010-03-03", 
                                               beforeTime="2009-12-31")), 0)

   # .........................................
   def test_listDefaults(self):
      self.cl.rad.listShapegrids()

   # .........................................
   def test_listWithParameters(self):
      self.cl.rad.listShapegrids(cellSides=6)

   # .........................................
   def test_postInvalid(self):
      self.assertRaises(Exception, 
                        self.cl.rad.postShapegrid, None, filename=None)

   # .........................................
   def test_postValidNoCutout(self):
      shpName = "utNC%s" % str(gmt().mjd)
      cellShape = "square"
      cellSize = "2.5"
      mapUnits = "dd"
      epsgCode = 4326
      bbox = "-50,0,-30,40"
      self.cl.rad.postShapegrid(shpName, cellShape, cellSize, mapUnits, epsgCode, bbox)
   
   # .........................................
   def test_postValidWithCutout(self):
      shpName = "utCut%s" % str(gmt().mjd)
      cellShape = "hexagon"
      cellSize = "12000"
      mapUnits = "meters"
      epsgCode = "3410"
      bbox = "2395830,469300,2506900,580350"
      cutout = "POLYGON((2395842.580000 580315.200000,2506842.580000 580315.200000,2506842.580000 469315.200000,2395842.580000 469315.200000,2395842.580000 580315.200000))"
      self.cl.rad.postShapegrid(shpName, cellShape, cellSize, mapUnits, epsgCode, bbox, cutout=cutout)

# .............................................................................
class TestOtherFunctions(unittest.TestCase):
   """
   @summary: Test class that tests other functions in the RAD client
   """
   # .........................................
   def setUp(self):
      self.cl = LMClient(userId=UT_USER, pwd=UT_PWD)

   # .........................................
   def tearDown(self):
      self.cl.logout()

   # .........................................
   def test_getStatusStageInvalid(self):
      expId = self.cl.rad.listExperiments(perPage=1)[0].id
      exp = self.cl.rad.getExperiment(expId)
      status, stage = self.cl.rad.getStatusStage(exp)
      self.assertIs(status, None)
      self.assertIs(stage, None)
   
   # .........................................
   def test_getStatusStageBucket(self):
      expId, bktId = getNewExpBkt(self.cl)
      bck = self.cl.rad.getBucket(expId, bktId)
      status, stage = self.cl.rad.getStatusStage(bck)
   
   # .........................................
   def test_getStatusStagePamSum(self):
      expId, bktId = getNewExpBkt(self.cl)
      self.cl.rad.intersectBucket(expId, bktId)
      #psId = self.cl.rad.listPamSums(expId, bktId, perPage=1)[0].id
      ps = self.cl.rad.getPamSum(expId, bktId, "original")
      status, stage = self.cl.rad.getStatusStage(ps)

# .............................................................................
def getNewExpBkt(cl):
   """
   @summary: Posts a new experiment and creates a bucket
   @return: Tuple with (experiment id, bucket id)
   """
   expName = "utExpBkt%s" % str(gmt().mjd)
   epsgCode = 4326
   # Create experiment
   exp = cl.rad.postExperiment(expName, epsgCode)
   lyr1 = cl.rad.postRaster('utRst1%s' % str(gmt().mjd), epsgCode=epsgCode, 
            filename=os.path.join('..', 'sampleData', 'demoLayer.tif'))
   lyr2 = cl.rad.postVector('utVec1%s' % str(gmt().mjd),
            filename=os.path.join('..', 'sampleData', 'radData', 
                                  'unitTestShape.shp'))
   # Add layers
   cl.rad.addPALayer(exp.id, lyr1.id, 'pixel', 120, 254, 30)
   cl.rad.addPALayer(exp.id, lyr2.id, 'PRESENCE', 1, 2, 30)

   # Create bucket
   cl.rad.addBucket(exp.id, 'utBkt1%s' % str(gmt().mjd), 'square', 1, 
                          'dd', epsgCode, '-180,0,0,90')
   bktId = cl.rad.listBuckets(exp.id)[0].id
   return exp.id, bktId

# .............................................................................
def getNewExpBktWithPamsums(cl):
   """
   @summary: Creates a new experiment and then adds PAM Sums to it for testing
   """
   expId, bktId = getNewExpBkt(cl)
   cl.rad.randomizeBucket(expId, bktId, method='splotch')
   cl.rad.intersectBucket(expId, bktId)
   cl.rad.randomizeBucket(expId, bktId, method='swap')
   cl.rad.randomizeBucket(expId, bktId, method='swap')
   cl.rad.randomizeBucket(expId, bktId, method='swap')
   return expId, bktId

# .............................................................................
def getTestSuites():
   """
   @summary: Gets the test suites for the module
   @return: A list of test suites
   """
   testSuites = []
   loader = unittest.TestLoader()
   testSuites.append(loader.loadTestsFromTestCase(TestRADLayers))
   testSuites.append(loader.loadTestsFromTestCase(TestRADShapegrids))
   testSuites.append(loader.loadTestsFromTestCase(TestRADExperiments))
   testSuites.append(loader.loadTestsFromTestCase(TestRADBuckets))
   testSuites.append(loader.loadTestsFromTestCase(TestRADExpPALayers))
   testSuites.append(loader.loadTestsFromTestCase(TestOtherFunctions))
   return testSuites

# ============================================================================
# = Main                                                                     =
# ============================================================================

if __name__ == '__main__':
   unittest.main()
