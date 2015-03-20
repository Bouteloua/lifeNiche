import cPickle, datetime
import sys, os, glob
from lifemapper.lmClientLib import LMClient
from password import *


def main():
	global cl
	cl = LMClient(userId=userName, pwd=password)

	path = "../views/experimentOutput/"
	if not os.path.exists(path):
		os.makedirs(path)

	experimentDict = loadExperiments()
	getExperimentAndProj(experimentDict, path)

def getExperimentAndProj(experimentDict, path):
	lenPastExperiments = len(experimentDict)
	count = 1
	for key, experiment in experimentDict.iteritems():
		experimentID = experiment['id']
		currentTime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
		FMT = '%Y-%m-%d %H:%M:%S'

		try:
			experimentPath = path + key +'-'+ experimentID + '.zip'
			print 'Downloading', count, 'out of', lenPastExperiments, 'experiments:', key, '->', experiment['id']
			cl.sdm.getExperimentPackage(experimentID, filename=experimentPath)
			unzipFile = "unzip -qd %s %s" % (experimentPath[:-4], experimentPath)
			os.system(unzipFile)
			deletedFiles = 'rm %s' % (experimentPath)
			os.system(deletedFiles)

			projPath = experimentPath[:-4] + '/projections/'
			if not os.path.exists(projPath):
				os.makedirs(projPath)
			print '\tGetting lifemapper projections IDs for:', key
			expProjs = cl.sdm.getExperiment(experiment['id'])
			for expProj in expProjs.projections:
				print '\tDownloading projections...', expProj.scenarioCode.split('-')[1], '->', expProj.id
				continue
				try:
					cl.sdm.getProjectionTiff(expProj.id, filename=projPath + expProj.speciesName +'-'+  expProj.id +'-'+ expProj.scenarioCode +'.tif')
				except:
					projLifeMapperTime = experiment['statusModTime']
					tdeltaProj = datetime.datetime.strptime(currentTime, FMT) - datetime.datetime.strptime(projLifeMapperTime, FMT)
					print '\t\tFAILED cannot download projection:', expProj.scenarioCode.split('-')[1], "->" , expProj.id, '\n\tLAPSES in time from posted projections to lifemapper ->', str(tdeltaProj)

		except:
			ExpLifemapperTime = experiment['createTime']
			tdeltaExp = datetime.datetime.strptime(currentTime, FMT) - datetime.datetime.strptime(ExpLifemapperTime, FMT)
			print '\tFAILED cannot download experiment:', key, "->", experiment['id'],'\n\tLAPSES in time from posted experiment to lifemapper ->', str(tdeltaExp)
			pass
		count += 1


def loadExperiments():
	'''Load the pickle file of scenario'''
	with open('../views/pastPickleDictionaries/experimentDictionary_2015-03.pickle') as f:
		expDic = cPickle.load(f)
	return expDic

if __name__ == '__main__':
	main()
