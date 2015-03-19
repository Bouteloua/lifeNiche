import cPickle, os, glob, datetime
import csv as c

def main():
	layersdictionary = recursionLayersPost(rawMetaData(), rawMetaData())
	#print layersdictionary




	#recursionLayerDic = pickleFilesLayersAndOccurr()
	#deletedCorrelatedLayers = pickleFilesLayersAndOccurr()

	#recursionTypeCodeID(layers)
	#delLayerDictionary = []
	#temp, deletedCorrelatedLayers = removeCorrelatedLayers(recursionLayerDic, deletedCorrelatedLayers)

	#print type(deletedCorrelatedLayers)


def recursionLayersPost(recurSearchLayerDic, masterLayersDic):
	'''The "postLayer" function allows you to post a new environmental layer to be used in your SDM experiments.'''
	fullMasterLayersDic = masterLayersDic
	if type(recurSearchLayerDic)==type({}):
		for key in recurSearchLayerDic:
			if key == 'fullname':
				print "cl.sdm.postLayer(name=%s, epsgCode=%s, envLayerType=%s, units=%s, dataFormat=%s, fileName=%s, title=%s, description=layerName%s, isCategorical=False)" % (recurSearchLayerDic['fullname'], recurSearchLayerDic['epsgCode'], recurSearchLayerDic['typeCode'], recurSearchLayerDic['units'], recurSearchLayerDic['dataFormat'], recurSearchLayerDic['filePath'], recurSearchLayerDic['title'], recurSearchLayerDic['layerDescription'])
				lyrObj = cl.sdm.postLayer(name=recurSearchLayerDic['fullname'],
										  epsgCode=recurSearchLayerDic['epsgCode'],
										  envLayerType=recurSearchLayerDic['typeCode'],
										  units=recurSearchLayerDic['units'],
										  dataFormat=recurSearchLayerDic['dataFormat'],
										  fileName=recurSearchLayerDic['filePath'],
										  title=recurSearchLayerDic['title'],
										  description=recurSearchLayerDic['layerDescription']
										  )
				#Updating the recurSearchLayerDic with the new lifemapper ID for that layer
				fullMasterLayersDic[recurSearchLayerDic['model']][recurSearchLayerDic['bioclim']][recurSearchLayerDic['typeCode']].update({'lyrID':9999999999})

			else:
				recursionLayersPost(recurSearchLayerDic[key], masterLayersDic)
	#Save a pickle file of the layer IDs
	with open('../views/pastPickleDictionaries/' + 'LayerDictionary.pickle', 'wb') as f:
		cPickle.dump(fullMasterLayersDic, f)
	return fullMasterLayersDic



def rawMetaData():
	print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
	'''Creates a dictionary off the metadata in the filename of the GTiff'''
	folderFiles = glob.glob('../views/GTiff/*.tif')

	#Check list of NULL
	if not folderFiles:
		print "No files in the folder", folderFiles
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
				'Name': index,
				'filterType': layernMetaData[layerName]['filterType'],
				'typeCode': layernMetaData[layerName]['typeCode'].lower(),
				'typeCodeDescription': layernMetaData[layerName]['TypeCodeDescription'],
				'projectionDate': layernMetaData[layerName]['ProjectionDate'],
				'layerDescription': layernMetaData[layerName]['LayerDescription'],
				'RCP': layernMetaData[layerName]['RCP'],
				'Correlated': layernMetaData[layerName]['Correlated'],
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


def readLayerMetaData():
	'''Open the the file layerMetaData.csv to get all the label meta data that cannot get out of the file name. Return a dictionary'''
	with open('../views/layerDescriptions/layerMetaData.csv', mode='r') as infile:
		reader = c.reader(infile)
		mydict = {rows[0].lower(): {'filterType': rows[1], 'typeCode': rows[2], 'TypeCodeDescription': rows[3], 'LayerDescription': rows[4], 'ProjectionDate': rows[5], 'RCP': rows[6], 'Correlated': rows[7]} for rows in reader}
	return mydict























def pickleFilesLayersAndOccurr():
	'''Load the pickle file of layerName'''
	path = '../views/pastPickleDictionaries/.masterLayerDictionary.pickle'
	if os.path.exists(path):
		with open('../views/pastPickleDictionaries/.masterLayerDictionary.pickle') as f:
			LayerDictionary = cPickle.load(f)
	else:
		print 'missing file!!!!!', path
		sys.exit()
	return LayerDictionary


def removeCorrelatedLayers(recursionLayerDic, deletedCorrelatedLayers):
	'''The "postLayer" function allows you to post a new environmental layer to be used in your SDM experiments.'''
	newDic = deletedCorrelatedLayers
	print 'newDic', type(newDic)
	if type(recursionLayerDic)==type({}):
		for key in recursionLayerDic:
			if key == 'Correlated' and recursionLayerDic[key] == 'yes':
				del newDic[recursionLayerDic['model']][recursionLayerDic['bioclim']][recursionLayerDic['typeCode']]
				#print 'deleting correlated layer...', recursionLayerDic['fullname']
			else:
				removeCorrelatedLayers(recursionLayerDic[key], deletedCorrelatedLayers)
	return recursionLayerDic, deletedCorrelatedLayers

def recursionTypeCodeID(typeCodeDictionary, typeCodeList):
	if type(typeCodeDictionary)==type({}):
		for key in typeCodeDictionary:
			if key == 'typeCode':
				if typeCodeDictionary[key] not in typeCodeList:
					typeCodeList.append(typeCodeDictionary[key])
			else:
				recursionTypeCodeID(typeCodeDictionary[key], typeCodeList)
	return typeCodeList


def listRemoveCorrelatedLayers(layerDictionary, delLayerDictionary):
	'''The "postLayer" function allows you to post a new environmental layer to be used in your SDM experiments.'''

	if type(layerDictionary)==type({}):
		for key in layerDictionary:
			if key == 'Correlated' and layerDictionary[key] == 'yes':
				if layerDictionary['fullname'] not in delLayerDictionary:
					delLayerDictionary.append(layerDictionary['fullname'])
			else:
				listRemoveCorrelatedLayers(layerDictionary[key], delLayerDictionary)
	return layerDictionary

if __name__ == '__main__':
	main()

