import cPickle, os

def main():
	recursionLayerDic = pickleFilesLayersAndOccurr()
	deletedCorrelatedLayers = pickleFilesLayersAndOccurr()

	#recursionTypeCodeID(layers)
	delLayerDictionary = []
	temp, deletedCorrelatedLayers = removeCorrelatedLayers(recursionLayerDic, deletedCorrelatedLayers)

	print type(deletedCorrelatedLayers)


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

