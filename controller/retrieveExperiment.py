import cPickle
import sys, os, glob
from lifemapper.lmClientLib import LMClient
from password import *

def main():
	global cl
	cl = LMClient(userId=userName, pwd=password)

	path = "../views/experimentOutput/"
	if not os.path.exists(path):
		os.makedirs(path)

	experimentDic = loadExperiments()
	downloadExperiments(experimentDic, path)
	#unzipExperiments(experimentDic, path)

def downloadExperiments(experimentDic, path):
	lenghtOfExpDic = len(experimentDic)
	count = 1
	for key, experiment in experimentDic.iteritems():
		zipfile = experiment['id']
		try:
			temp = str(path + key +'-'+ zipfile + '.zip')
			cl.sdm.getExperimentPackage(experiment['id'], filename=temp)
			print 'Downloaded', count, 'out of', lenghtOfExpDic, 'experiments ->', key, experiment['id']
		except:
			print 'Error from:', key, experiment['id']
			count += 1
			pass
		count += 1
		unzipFile = "unzip -qd %s %s" % (temp[:-4], temp)
		os.system(unzipFile)
		deleted = 'rm %s' % (temp)
		os.system(deleted)

def loadExperiments():
	'''Load the pickle file of scenario'''
	with open('../views/pickleDic/expDic.pickle') as f:
		expDic = cPickle.load(f)
	return expDic

if __name__ == '__main__':
	main()

