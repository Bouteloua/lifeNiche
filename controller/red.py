import cPickle, os

def main():
	layers = pickleFilesLayersAndOccurr()
	recursionTypeCodeID(layers)
	#recursionLayersPost(layers)


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


def recursionLayersPost(layerDictionary):
	'''The "postLayer" function allows you to post a new environmental layer to be used in your SDM experiments.'''

	if type(layerDictionary)==type({}):
		for key in layerDictionary:

			if key == 'fullname':
				print "cl.sdm.postLayer(name=%s, epsgCode=%s, envLayerType=%s, units=%s, dataFormat=%s, fileName=%s, title=%s, description=layerName%s, isCategorical=False)" % (layerDictionary['fullname'], layerDictionary['epsgCode'], layerDictionary['typeCode'], layerDictionary['units'], layerDictionary['dataFormat'], layerDictionary['filePath'], layerDictionary['title'], layerDictionary['layerDescription'])
				lyrObj = cl.sdm.postLayer(name=layerDictionary['fullname'],
										  epsgCode=layerDictionary['epsgCode'],
										  envLayerType=layerDictionary['typeCode'],
										  units=layerDictionary['units'],
										  dataFormat=layerDictionary['dataFormat'],
										  fileName=layerDictionary['filePath'],
										  title=layerDictionary['title'],
										  description=layerDictionary['layerDescription']
										  )
				# Updating the layerDictionary with the new lifemapper ID for that layer
				layerDictionary.update({'lyrID':lyrObj.id})
			else:
				recursionLayersPost(layerDictionary[key])
		#Save a pickle file of the layer IDs
	with open('../views/pastPickleDictionaries/' + 'LayerDictionary' + '.pickle', 'wb') as f:
		cPickle.dump(layerDictionary, f)
	return layerDictionary

def recursionTypeCodeID(typeCodeDictionary):
	if type(typeCodeDictionary)==type({}):
		for key in typeCodeDictionary:
			if key == 'typeCode':
				if typeCodeDictionary[key] not in typeCodeList:
					typeCodeList.append(typeCodeDictionary[key])
			else:
				recursionTypeCodeID(typeCodeDictionary[key], typeCodeList)
	return typeCodeList



if __name__ == '__main__':
	main()

