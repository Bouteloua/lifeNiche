import glob, sys, os, commands, fiona, cPickle, datetime
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
		print 'updating codeType... %s' % typecode.lower()

		#Creates a typecode dictionary of all the typecode that got uploaded to lifemapper
		typeCodeDictionary.setdefault(typecode, {
		'code': typecode,
		'created_at': datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'),
		})
	#print postDicLayers
	##Save a pickle dictionary of all the typecodes
	with open('../views/pickleDic/' + 'typeCodeDictionary' + '.pickle', 'wb') as f:
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
			print 'Check the layerMetaData.csv file in the rawMetaData folder. MISSING DATA!!!!!!!!'
			sys.exit()

	return filenameDic



def updateLyrsIDs(rawData):

	lyrs = cl.sdm.listLayers(epsgCode=4326, perPage=500, public=False)

	cl.sdm.countLayers(epsgCode=4326)

	cleanupDic = {}
	count = 0
	for i in lyrs:
	    cleanupDic[i.title.split(': ')[1].strip()] = i.id

	count = 0
	for bioClimKey, value in rawData.iteritems():
		for scenarioKey, value1 in value.items():
			for typeCode_key, layerName in value1.items():
				if layerName['title'] in cleanupDic:
					t = layerName['title']
					rawData[bioClimKey][scenarioKey][typeCode_key].update({'lyrID':cleanupDic[t]})
					print 'Updating layer ID...', rawData[bioClimKey][scenarioKey][typeCode_key]['fullname']
					count += 1

	with open('../views/pickleDic/' + '.masterLayerDictionary' + '.pickle', 'wb') as f:
		cPickle.dump(rawData, f)

	count = cl.sdm.countLayers(epsgCode=4326)

	print 'Total layer count uploaded onto lifemapper:', count
	print 'Total layer count uploaded in .masterLayerDictionary.pickle file', count


############################# END START LOAD OLD FILES ######################################


def readLayerMetaData():
	'''Open the the file layerMetaData.csv to get all the label meta data that cannot get out of the file name. Return a dictionary'''
	with open('../views/rawMetaData/layerMetaData.csv', mode='r') as infile:
		reader = c.reader(infile)
		mydict = {rows[0].lower(): {'filterType': rows[1], 'typeCode': rows[2], 'TypeCodeDescription': rows[3], 'LayerDescription': rows[4], 'ProjectionDate': rows[5], 'RCP': rows[6]} for rows in reader}
		#print mydict
	return mydict

def newOrOldFiles():
	'''Upload new data or load the past pickle files'''
	#THINGS THAT CHANGE
	#####################################
	#Add values to to the index
	#If you rerun increase this number to avoid unique id collisions
	passwordSetAndUqiValue()
	rawData = rawMetaData()
	postTypeCode(rawData)
	updateLyrsIDs(rawData)



if __name__ == '__main__':
	main()
