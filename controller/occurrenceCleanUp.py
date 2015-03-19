import os, sys
import cPickle as cp
from lifemapper.lmClientLib import LMClient
import csv as c


from password import *

def main():
	global cl
	cl = LMClient(userId=userName, pwd=password)

	pickListOptions()

def pickListOptions():

	whileOccurrenceClean = True
	while whileOccurrenceClean:
		print 'Only need to update master occurrence dictionary if you updated new occurrence files into Lifemapper or not picklist'
		inputType = raw_input('Update the "MASTER" occurrence dictionary or just species "PICKLIST" dictionary: ')
		if inputType.lower() == 'master':
			print 'Updating the master and picklist dictionary'
			updateMasterOccurrence()
			updatePickList()
			whileOccurrenceClean = False
		elif inputType.lower() == 'picklist':
			print 'Updating only the species picklist dictionary'
			updatePickList()
			whileOccurrenceClean = False
		else:
			whileOccurrenceClean = True

def pickleFileOccurrence():
	'''Load the pickle file of occurrence'''
	path = '../views/pastPickleDictionaries/.masterOccurrenceDictionary.pickle'
	if os.path.exists(path):
		with open('../views/pastPickleDictionaries/.masterOccurrenceDictionary.pickle') as f:
			occurrenceDictionary = cp.load(f)
	else:
		print 'missing file!!!!!', path
		sys.exit()
	return occurrenceDictionary


def updatePickList():

	occPickList = occurrencePickList()
	occurrenceDictionary = pickleFileOccurrence()
	pickList = dict([(i, occurrenceDictionary[i]) for i in occPickList if i in occurrenceDictionary])

			#Save a pickle file of the occurrence IDs
	with open('../views/pastPickleDictionaries/' + 'occurrenceDictionary' + '.pickle', 'wb') as f:
		cp.dump(pickList, f)

	print '\nOccurrence dictionary of %s records are ready for posting experiments\ntime to run mapper.py' % len(pickList)

def updateMasterOccurrence():
	perPageTotal = 20000
	epsgCodeL = 4326
	print 'Getting a list no greater than %s occurrences records for all %s "epsg code" occurrences' % (perPageTotal, epsgCodeL)
	occurrenceObjs = cl.sdm.listOccurrenceSets(epsgCode=epsgCodeL, perPage=perPageTotal)

	occurrenceDictionary = dict()
	speciesMetaFile = readLayerMetaData()
	countSpeciesMatch = 0
	countNOSpeciesMatch = 0
	for occurrenceObj in occurrenceObjs:

		if occurrenceObj.title[:8].lower() == 'uploaded':
			occurrenceObj.title = occurrenceObj.title[8:]

		if occurrenceObj.title.lower() == 'caede':
			continue

		species = occurrenceObj.title
		if species.lower() in speciesMetaFile:
			occurrenceDictionary.setdefault(species, {
					'epsgCode': int(occurrenceObj.epsgcode),
					'occurrenceID': occurrenceObj.id,
					'species': species,
					'dataFormat': speciesMetaFile[species.lower()]['shapefile'],
					'occurencesCount': speciesMetaFile[species.lower()]['occurencesCount'],
					'downloadedTime': speciesMetaFile[species.lower()]['downloadedTime'],
					'family': speciesMetaFile[species.lower()]['family'],
					'group': int(speciesMetaFile[species.lower()]['group'])
					})
			countSpeciesMatch += 1
		else:
			occurrenceDictionary.setdefault(species, {
				'epsgCode': int(occurrenceObj.epsgcode),
				'occurrenceID': occurrenceObj.id,
				'species': species,
				'shapefile': 'NULL',
				'occurencesCount': 'NULL',
				'downloadedTime': 'NULL',
				'family': 'NULL',
				'group': -9999,
				})
			print 'could not match', species
			countNOSpeciesMatch += 1
	print 'The number of records on lifemapper', cl.sdm.countOccurrenceSets(epsgCode=epsgCodeL)
	print 'The number of matches:', countSpeciesMatch
	print 'The number of missing matches:', countNOSpeciesMatch

	path = '../views/pastPickleDictionaries/'
	hiddenPaths = filter( lambda f:  f.startswith('.'), os.listdir(path +'.'))
	for hiddenfile in hiddenPaths:
		if hiddenfile == '.masterOccurrenceDictionary.pickle':
			os.system("rm ../views/pastPickleDictionaries/.masterOccurrenceDictionary.pickle")
		if hiddenfile == '.master_OccurrenceDictionary.pickle':
			os.system("rm ../views/pastPickleDictionaries/.master_OccurrenceDictionary.pickle")

		#Save a pickle file of the occurrence IDs
	with open('../views/pastPickleDictionaries/' + '.masterOccurrenceDictionary' + '.pickle', 'wb') as f:
		cp.dump(occurrenceDictionary, f)
	print 'Completed %s records into .masterOccurrenceDictionary.pickle' % countSpeciesMatch
	return occurrenceDictionary

def occurrencePickList():
	'''Open the the file speciesDistributionmetaData.csv to get all the label meta data that cannot get out of the file name. Return a dictionary'''
	with open('../views/layerDescriptions/occurrencePickList.csv', mode='r') as infile:
		reader = c.reader(infile)
		speciesHolder = []
		for i in reader:
			speciesHolder.append(i[0])
	return speciesHolder

def readLayerMetaData():
	'''Open the the file speciesDistributionmetaData.csv to get all the label meta data that cannot get out of the file name. Return a dictionary'''
	with open('../views/layerDescriptions/speciesDistributionmetaData.csv', mode='r') as infile:
		reader = c.reader(infile)
		mydict = {rows[0].lower(): {'shapefile': rows[1], 'occurencesCount': rows[2], 'downloadedTime': rows[3], 'family': rows[4], 'bonapID': rows[5], 'group': rows[6]} for rows in reader}
	return mydict



if __name__ == '__main__':
	main()
