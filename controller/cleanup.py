import glob, sys, os, commands, fiona, cPickle, datetime, os.path
import csv as c
import pandas as pd
#from lifemapper.lmClientLib import LMClient
from shapely.geometry import Point, mapping
from lifemapper.lmClientLib import LMClient
#Change to match your lifemapper ID and password
from password import *
import time


def main():
	newOrOldFiles()
#cl.sdm.getExperimentPackage(1399743, filename='/home/franzone/Documents/lifeNiche/views/1399744.zip')
###########################THIS WILL NEED TO CHANGE#######################################
def passwordSetAndUqiValue():
	'''This is userName and passwords and unique ID'''
	global cl
	#Setup your client ID and password in the file named password.py

	cl = LMClient(userId=userName, pwd=password)



############################## POST TYPECODE ############################################
def postTypeCode(postDicLayers):
	'''The "postTypeCode" function allows you to post a new type code to be used for matching environmental layers.
	 This post request can be as simple as just adding a character string identifying it. '''
		# postTypeCode(
		# 	code-> The code to use for this new type code [string]
		# 	title-> (optional) A title for this type code [string]
		# 	description -> (optional) An extended description of this type code [string]
		# 	)

	#Dictionary holding the unique typecodes
	typeCodeDictionary = dict()

	typeList = []
	#Make a list of all the typecode values
	for bioClimKey, value in postDicLayers.iteritems():
		for scenarioKey, value1 in value.items():
			for typeCode_key, layerName in value1.items():
				typeList.append(typeCode_key)

	#Iterate through all the unique set list of typecodes
	for typecode in set(typeList):
		#Creates a typecode dictionary of all the typecode that got uploaded to lifemapper
		typeCodeDictionary.setdefault(typecode, {
		'code': typecode,
		'created_at': datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'),
		})

		print 'Updated unique type code... %s' % typecode.lower()
	#print postDicLayers
	##Save a pickle dictionary of all the typecodes
	with open('../views/pastPickleDictionaries/' + 'typeCodeDictionary' + '.pickle', 'wb') as f:
		cPickle.dump(typeCodeDictionary, f)

#Creates the data structures for the layers
def rawMetaData():
	'''Creates a dictionary off the metadata in the filename of the GTiff'''
	folderFiles = glob.glob('../views/GTiff/*.tif')

	#Check list of NULL
	if not folderFiles:
		print "File list is empty"
		sys.exit(0)


	filenameDic = dict()
	layernMetaData = readLayerMetaData()
	for index, folderFile in enumerate(folderFiles):

		typeCode = folderFile.split(".")[4].strip()

		layerName = folderFile.split("/")[3][:-4].strip().lower()
		layer = folderFile.split(".")[3] + '.' + folderFile.split(".")[4].strip()
		bioclim = layer.split('.')[0].strip()
		title = folderFile.split("/")[3].strip()
		model = title.split('.')[0].strip()
		fullname = folderFile.split("/")[3][:-4].strip()

		if layerName in layernMetaData.keys():
			filenameDic.setdefault(model, {}).setdefault(bioclim, {}).setdefault(typeCode, {
				# remove the index + X
				'Name': index,
				'filterType': layernMetaData[layerName]['filterType'],
				'typeCode': layernMetaData[layerName]['typeCode'].lower(),
				'typeCodeDescription': layernMetaData[layerName]['TypeCodeDescription'],
				'projectionDate': layernMetaData[layerName]['ProjectionDate'],
				'layerDescription': layernMetaData[layerName]['LayerDescription'],
				'RCP': layernMetaData[layerName]['RCP'],
				'bioclim': bioclim,
				'epsgCode': 4326,
				'envLayerType': layer,
				'units': 'dd',
				'model': model,
				'dataFormat': 'GTiff',
				'filePath': folderFile,
				'title': title,
				'fullname': fullname,
				'resolution': '30',
				'created_at': datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'),
				})
		else:
			print '**********************************error***************************************'
			print 'Check the layerMetaData.csv file in the layerDescriptions folder. MISSING DATA!!!!!!!!'
			sys.exit()

	return filenameDic



def updateLyrsIDs(rawData):

	lyrs = cl.sdm.listLayers(epsgCode=4326, perPage=500, public=False)

	cl.sdm.countLayers(epsgCode=4326)

	cleanupDic = {}
	count = 0
	for i in lyrs:
	    cleanupDic[i.title.split(': ')[1].strip()] = i.id

	updateCounter = 0
	for bioClimKey, value in rawData.iteritems():
		for scenarioKey, value1 in value.items():
			for typeCode_key, layerName in value1.items():
				if layerName['title'] in cleanupDic:
					temp = layerName['title']
					rawData[bioClimKey][scenarioKey][typeCode_key].update({'lyrID':cleanupDic[temp]})
					print 'Updated layer ID:', rawData[bioClimKey][scenarioKey][typeCode_key]['fullname']
					updateCounter += 1

	path = '../views/pastPickleDictionaries/'
	hiddenPaths = filter( lambda f:  f.startswith('.'), os.listdir(path +'.'))
	for hiddenfile in hiddenPaths:
		if hiddenfile == '.masterLayerDictionary.pickle':
			os.system("rm ../views/pastPickleDictionaries/.masterLayerDictionary.pickle")
		if hiddenfile == '.master_LayerNameDictionary.pickle':
			os.system("rm ../views/pastPickleDictionaries/.master_LayerNameDictionary.pickle")

	with open('../views/pastPickleDictionaries/' + '.masterLayerDictionary' + '.pickle', 'wb') as f:
		cPickle.dump(rawData, f)

	LifeMapperCount = cl.sdm.countLayers(epsgCode=4326)

	if LifeMapperCount == updateCounter:
		print "\nLifemapper and your personal dictionaries are in sync!!!, it's safe to post experiments now\n"
	else:
		print "\nLifemapper and your personal dictionaries are out of sync!!!!. Something is wrong"
		print "This could be correct if your doing this for a set purpose to remove layers and then running mapper.py\n"

	print 'Current total of layers uploaded on lifemapper:', LifeMapperCount
	print 'Current total of layers uploaded on .masterLayerDictionary.pickle file', updateCounter


############################# END START LOAD OLD FILES ######################################


def readLayerMetaData():
	'''Open the the file layerMetaData.csv to get all the label meta data that cannot get out of the file name. Return a dictionary'''
	with open('../views/layerDescriptions/layerMetaData.csv', mode='r') as infile:
		reader = c.reader(infile)
		mydict = {rows[0].lower(): {'filterType': rows[1], 'typeCode': rows[2], 'TypeCodeDescription': rows[3], 'LayerDescription': rows[4], 'ProjectionDate': rows[5], 'RCP': rows[6]} for rows in reader}
		#print mydict
	return mydict

def newOrOldFiles():
	'''Upload new data or load the past pickle files'''
	passwordSetAndUqiValue()
	rawData = rawMetaData()
	postTypeCode(rawData)
	updateLyrsIDs(rawData)



if __name__ == '__main__':
	main()
