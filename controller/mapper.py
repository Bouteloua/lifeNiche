import glob, sys, os, commands, fiona, cPickle
import csv as c
import pandas as pd
from lifemapper.lmClientLib import LMClient
from shapely.geometry import Point, mapping
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
	#Need to be an unique number within accout index
	uniqid = 'b2'
	return uniqid

#ONLY FOR CURRENT!!
# def postTypeCode(postDicLayers):
# 	'''The "postTypeCode" function allows you to post a new type code to be used for matching environmental layers.
# 	 This post request can be as simple as just adding a character string identifying it. '''
# 		# postTypeCode(
# 		# 	code-> The code to use for this new type code [string]
# 		# 	title-> (optional) A title for this type code [string]
# 		# 	description -> (optional) An extended description of this type code [string]
# 		# 	)
# 	typeCodeDic = dict()
# 	print postDicLayers

# 	for typecode in postDicLayers['current'].keys():
# 		#print typecode

# 		#tc = cl.sdm.postTypeCode(code=typecode.lower(),
# 								#title=typecode.upper(),
# 								#description=postDicLayers['current'][typecode]['typeCodeDescription'])

# 		typeCodeDic.setdefault(typecode, {
# 			# remove the index + X
# 			'code': typecode,
# 			'title': typecode.upper(),
# 			'description': postDicLayers['current'][typecode]['typeCodeDescription'],
# 			})

# 	print typeCodeDic
# 	print 'time to quick'
# 	sys.exit(0)
# 	with open('../views/pickleDic/' + 'typeCode_dict' + '.pickle', 'wb') as f:
# 		cPickle.dump(typeCodeDic, f)



############################## POST TYPECODE ############################################
def postTypeCode(postDicLayers):
	'''The "postTypeCode" function allows you to post a new type code to be used for matching environmental layers.
	 This post request can be as simple as just adding a character string identifying it. '''
		# postTypeCode(
		# 	code-> The code to use for this new type code [string]
		# 	title-> (optional) A title for this type code [string]
		# 	description -> (optional) An extended description of this type code [string]
		# 	)
	typeCodeDic = dict()

	typeList = []
	for key, typeCode in postDicLayers.iteritems():
		for key1, value in typeCode.items():
			typeList.append(key1)


	for typecode in set(typeList):
		print 'tc = cl.sdm.postTypeCode(code=%s)' % typecode.lower()
		tc = cl.sdm.postTypeCode(code=typecode.lower())

		typeCodeDic.setdefault(typecode, {
		# remove the index + X
		'code': typecode,
		})

	with open('../views/pickleDic/' + 'typeCode_dict' + '.pickle', 'wb') as f:
		cPickle.dump(typeCodeDic, f)
############################## POST TYPECODE ###########################################

################################# POST LAYERS ##########################################
def postLayers(postDicLayers):
	'''The "postLayer" function allows you to post a new environmental layer to be used in your SDM experiments.
	It takes a number of parameters. More information about these parameters is available in the code documentation.'''
	for key, layerNames in postDicLayers.iteritems():
		for key1, layerName in layerNames.items():
			print "cl.sdm.postLayer(name=%s, epsgCode=%s, envLayerType=%s, units=%s, dataFormat=%s, fileName=%s, title=%s, description=layerName%s, isCategorical=False)" % (layerName['fullname'], layerName['epsgCode'], layerName['typeCode'], layerName['units'], layerName['dataFormat'], layerName['filePath'], layerName['title'], layerName['layerDescription']) 
			lyrObj = cl.sdm.postLayer(name=layerName['fullname'],
									  epsgCode=layerName['epsgCode'],
									  envLayerType=layerName['typeCode'],
									  units=layerName['units'],
									  dataFormat=layerName['dataFormat'],
									  fileName=layerName['filePath'],
									  title=layerName['title'],
									  description=layerName['layerDescription']
									  )
	#isCategorical=False
			postDicLayers[key][key1].update({'lyrID':lyrObj.id})

	#Save a pickle file of the layer IDs
	
	with open('../views/pickleDic/' + 'layerName_dict' + '.pickle', 'wb') as f:
		cPickle.dump(postDicLayers, f)

	print '####### Completed loadup of layer IDs and TypeCode IDs see file layerName_dict.pickle for input ############\n'
	return postDicLayers

############################## END POST LAYERS ##########################################

############################## POST OCCURRENCE ##########################################
def postOccurrence():
	'''The "postOccurrenceSet" function allows you to add a new occurrence set for SDM experiments to the Lifemapper system.
	It takes a name, a file and file type as well as an option parameter for specifying the map
	projection (as an EPSG code) for your occurrence data.'''
	taxaFileExist = os.path.isfile('../views/rawMetaData/taxaList.csv')
	if taxaFileExist == True:
		print 'Loading csv file into shapefiles'
		occurrenceDic = csvToShapefile()
	else:
		print 'Loading Shapefiles'
		occurrenceDic = getShapeFiles()


	for key, occurrence in occurrenceDic.iteritems():
		print "cl.sdm.postOccurrenceSet(displayName=%s, fileType=%s, fileName=%s, epsgCode=%s)"  % (str(key), 'shapefile', occurrence['shpPath'], occurrence['epsgCode'])

		occObj = cl.sdm.postOccurrenceSet(displayName=str(key),
										  fileType='shapefile',
										  fileName=occurrence['shpPath'],
										  epsgCode=occurrence['epsgCode'])

		#Add the occurrence ID from lifemapper to the dictionary
		occurrenceDic[key].update({'occID':occObj.id})
	
	#Save a pickle file of the occurrence IDs
	with open('../views/pickleDic/' + 'occurrence_dict' + '.pickle', 'wb') as f:
		cPickle.dump(occurrenceDic, f)

	print '####### Completed loadup of occurrence IDs see file occurrence_dict.pickle for input ############\n'
	return occurrenceDic
############################## END POST OCCURRENCE ######################################

############################## POST SCENARIO ############################################
def postScenario(postDicLayers,uniqid):
	'''The "postScenario" function allows you to add a new scenario for creating SDM models and projections to the Lifemapper system.
	You will need to supply a few parameters at a minimum when posting a new scenario. More information about
	these parameters is available in the code documentation.'''

	scenarioDic = dict()
	resolution = 0
	count = 1
	units = 0
	epsgCode = 0

	envLayerID = []
	spatLayerID = []
	gmted2010ID = []

	try:
		for key, layerNames in postDicLayers['hwsd'].iteritems():
			envLayerID.append(postDicLayers['hwsd'][key]['lyrID'])
	except:
		print 'No hwsd files!!!!!!!!\n\n'
		pass

	try:
		for key, layerNames in postDicLayers['dist'].iteritems():
			spatLayerID.append(postDicLayers['dist'][key]['lyrID'])
	except:
		print 'No dist files!!!!!!!!\n\n'
		pass
	try:
		for key, layerNames in postDicLayers['gmted2010'].iteritems():
			gmted2010ID.append(postDicLayers['gmted2010'][key]['lyrID'])
	except:
		print 'No gmted2010 files!!!!!!!!\n\n'
		pass

	for key, layerNames in postDicLayers.iteritems():
		hold = []
		for key1, layerName in layerNames.items():
			if postDicLayers[key][key1]['base'] != 'clim':
				continue
			hold.append(postDicLayers[key][key1]['lyrID'])
			resolution = postDicLayers[key][key1]['resolution']
			units = postDicLayers[key][key1]['units']
			epsgCode = postDicLayers[key][key1]['epsgCode']
			base = postDicLayers[key][key1]['base']

		if key == 'dist' or key=='hwsd' or key == 'gmted2010':
			continue
		keyDic = 'Scenario' + uniqid + str(count) + '-' + key
		if keyDic.split('-')[1].lower() == 'current':
			currentID = keyDic
		#print 'Scenario Code:', keyDic, 'bioclim Key:', key,
		scenarioDic.setdefault(keyDic, {
			# remove the index + X
			'layers': hold + envLayerID + spatLayerID + gmted2010ID,
			'code': keyDic,
			'epsgCode': epsgCode,
			'units': units,
			'title': 'Climate Scenario' + key,
			'author': 'CGW',
			'resolution': resolution,
			'bioclim': key,
			'base':base
			})

		print "cl.sdm.postScenario(layers=%s, code=%s, epsgCode=%s, units=%s, title=%s, author=%s, resolution=%s)" % (hold + envLayerID + spatLayerID + gmted2010ID, keyDic, epsgCode, units, key + 'Climate Scenario', "CGW", resolution)
		scn = cl.sdm.postScenario(layers=hold + envLayerID + spatLayerID + gmted2010ID, code=keyDic, epsgCode=epsgCode, units=units, title=key + 'climate, env, spat, scenario', author="CGW", resolution=resolution)
		
		scenarioDic[keyDic].update({'scnID':scn.id})
			#Save a pickle file of the occurrence IDs

	#print postDicLayers
	with open('../views/pickleDic/' + 'scenario_dict' + '.pickle', 'wb') as f:
		cPickle.dump(scenarioDic, f)

	#print '####### Start of the Scenario ID dictionary ############'
	#print scenarioDic
	#print 'QUIT'
	#sys.exit()
	print '####### Completed loadup of scenario IDs see file scenario_dict.pickle for input ############\n'
	return scenarioDic, currentID
	print '#############################################################################################\n'
############################## END POST Scenario #########################################

############################## New POST Experiment ########################################
def newPostExperiment(scenarioDic, currentID, occurrences, alg):
	'''The "postExperiment" function allows you to post a new Lifemapper SDM experiment.'''
	

	prjScns_input = []
	for key, value in scenarioDic.iteritems():
		prjScns_input.append(value['scnID'])

	expDic = dict()
	for key, occurrence in occurrences.iteritems():
		
		print "cl.sdm.postExperiment(algorithm=%s, mdlScn=%s, occSetId=%s, prjScns=%s, name=%s, description=%s)" % (alg, scenarioDic[currentID]['scnID'], occurrence['occID'], prjScns_input, 'Test Experiment2', 'Test run2')
		exp = cl.sdm.postExperiment(algorithm=alg,
									mdlScn=scenarioDic[currentID]['scnID'],
									occSetId=occurrence['occID'],
									prjScns=prjScns_input,
									name='Experiment Name',
									description='Description data')

		expDic.setdefault(key, {
			# remove the index + X
			'bbox': exp.bbox,
			'createTime': exp.createTime,
			'description': exp.description,
			'epsgcode': exp.epsgcode,
			'id': exp.id,
			'metadataUrl': exp.metadataUrl,
			'modTime': exp.modTime,
			'statusModTime': exp.statusModTime,
			'user': exp.user,
			'speciesName': key,
			'prjScns': prjScns_input,
			'mdlScn': scenarioDic[currentID]['scnID'],
			'algorithm': alg,
			'occSetId': occurrence['occID'],
			})
		time.sleep(1)

	with open('../views/pickleDic/' + 'expDic' + '.pickle', 'wb') as f:
		cPickle.dump(expDic, f)

	print '####### Completed loadup of Experiment IDs see file expDic.pickle for input ############\n'
	print expDic
############################## new END POST Experiment ####################################

############################## old POST Experiment ########################################
def oldPostExperiment(scenarioDic, occurrences, alg):
	'''The "postExperiment" function allows you to post a new Lifemapper SDM experiment.'''
	prjScns_input = []
	print scenarioDic
	for key, value in scenarioDic.iteritems():
		prjScns_input.append(value['scnID'])

	current_layer_name = ''
	for keyOfLayerName in scenarioDic:
		Name = keyOfLayerName.split('-')
		if 'current' in Name:
			current_layer_name = keyOfLayerName

	expDic = dict()
	for key, occurrence in occurrences.iteritems():
		print prjScns_input
		print "cl.sdm.postExperiment(algorithm=%s, mdlScn=%s, occSetId=%s, prjScns=%s, name=%s, description=%s)" % (alg, scenarioDic[current_layer_name]['scnID'], occurrence['occID'], prjScns_input, 'Test Experiment2', 'Test run2')
		exp = cl.sdm.postExperiment(algorithm=alg,
									mdlScn=scenarioDic[current_layer_name]['scnID'],
									occSetId=occurrence['occID'],
									prjScns=prjScns_input,
									name='Test Experiment2',
									description='Test run2')

		expDic.setdefault(key, {
			# remove the index + X
			'bbox': exp.bbox,
			'createTime': exp.createTime,
			'description': exp.description,
			'epsgcode': exp.epsgcode,
			'id': exp.id,
			'metadataUrl': exp.metadataUrl,
			'modTime': exp.modTime,
			'statusModTime': exp.statusModTime,
			'user': exp.user,
			'speciesName': key,
			})
		time.sleep(1)

	with open('../views/pickleDic/' + 'expDic' + '.pickle', 'wb') as f:
		cPickle.dump(expDic, f)

	print '####### Completed loadup of Experiment IDs see file expDic.pickle for input ############\n'
	print expDic


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
		# typeCode = folderFile.split("_")[1][:-4].strip()
		# layerName = folderFile.split("/")[3][:-4].strip().lower()
		# layer = folderFile.split(".")[3].strip()
		# bioclim = layer.split("_")[0].strip()
		# title = folderFile.split("/")[3].strip()
		# base = title.split('.')[0].strip()
		# fullname = folderFile.split("/")[3][:-4].strip()

		typeCode = folderFile.split(".")[4].strip()

		layerName = folderFile.split("/")[3][:-4].strip().lower()
		layer = folderFile.split(".")[3] + '.' + folderFile.split(".")[4].strip()
		bioclim = layer.split('.')[0].strip()
		title = folderFile.split("/")[3].strip()
		base = title.split('.')[0].strip()
		fullname = folderFile.split("/")[3][:-4].strip()
		#print '*********************'
		#print layernMetaData['hwsd']

		if layerName in layernMetaData.keys():
			filenameDic.setdefault(bioclim, {}).setdefault(typeCode, {
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
				'base': base,
				'dataFormat': 'GTiff',
				'filePath': folderFile,
				'title': title,
				'fullname': fullname,
				'resolution': '30',
				})
		else:

			
			print '**********************************error***************************************'
			print 'Check the layerMetaData.csv file in the rawMetaData folder. MISSING DATA!!!!!!!!'
			sys.exit()

	return filenameDic


############################# START LOAD OLD FILES ######################################
def pickleFilesLayersAndOccurr():
	'''Load the pickle file of layerName'''
	with open('../views/pickleDic/layerName_dict.pickle') as f:
		lyrs = cPickle.load(f)
	return lyrs

def pickleFileOccurrence():
	'''Load the pickle file of occurrence'''
	with open('../views/pickleDic/occurrence_dict.pickle') as f:
		occurs = cPickle.load(f)
	return occurs


def pickleFileScenario():
	'''Load the pickle file of scenario'''
	with open('../views/pickleDic/scenario_dict.pickle') as f:
		scens = cPickle.load(f)
	return scens

############################# END START LOAD OLD FILES ######################################


#Take a csv file and makes returns shapefile for each unique species. Then returns a dictionary name, file path, and will add occurrence ID later
def csvToShapefile():
	'''Take a csv file and creates shapefiles'''
	schema = { 'geometry': 'Point', 'properties': { 'name': 'str:24'} }

	indivCsvOccurrList = '../views/indivCsvOccurrList/'
	shapefiles = '../views/shapefiles'

	#Creates a folder is shapefiles does not exist
	try:
		os.stat(indivCsvOccurrList)
	except:
		os.mkdir(indivCsvOccurrList)

	df = pd.read_csv('../views/rawMetaData/taxaList.csv')
	uniqueNames = df['taxa'].drop_duplicates()
	for uniqueName in uniqueNames:
		filename = df[(df['taxa']  == uniqueName)]
		filename.to_csv(indivCsvOccurrList + uniqueName + '.csv', index = False)

	#The output to all the individual species text files
	csvPath = indivCsvOccurrList

	#Creates a folder is shapefiles does not exist
	try:
		os.stat(shapefiles)
	except:
		os.mkdir(shapefiles)

	#The output to all the individual shapefiles
	shpOutBasePath = shapefiles
	#Column name for Longitude
	lonField = 'long'
	#Column name for Latitude
	latField = 'lat'
	#Column name for species names
	nameField = 'taxa'

	csvs = commands.getoutput('ls %s*.csv' % (csvPath))
	csvPathList = csvs.split('\n')

	shapefileDic = dict()

	for csv in csvPathList:
		spsName = os.path.basename(csv)
		shpOut = os.path.join(shpOutBasePath,spsName.replace('.csv','.shp'))
		shapefileDic.setdefault(csv.split("/")[3][:-4], {'shpPath': shpOut, 'epsgCode': '4326'})
		try:
			with fiona.open( shpOut, "w", "ESRI Shapefile", schema) as output:
				with open(csv, 'rb') as f:
					reader = c.DictReader(f)
					for row in reader:
						point = Point(float(row[lonField]), float(row[latField]))
						output.write({
						'properties': {
						'name': row[nameField]
						},
						'geometry': mapping(point)
						})
		except Exception, e:
			print "failed to write %s because %s" % (spsName,str(e))

	return shapefileDic

def getShapeFiles():
	'''Creates a dictionary off the metadata in the filename of the GTiff'''
	shapeFilePaths = glob.glob('../views/shapefiles/*.shp')
	shapefileDic = dict()
	for shapeFilePath in shapeFilePaths:
		shapefileDic.setdefault(shapeFilePath.split('/')[-1][:-4], {
			# remove the index + X
			'shpPath': shapeFilePath,
			'epsgCode': '4326',
			'species': shapeFilePath.split('/')[-1][:-4]
			})
	return shapefileDic

def readLayerMetaData():
	'''Open the the file layerMetaData.csv to get all the label meta data that cannot get out of the file name. Return a dictionary'''
	with open('../views/rawMetaData/layerMetaData.csv', mode='r') as infile:
		reader = c.reader(infile)
		mydict = {rows[0].lower(): {'filterType': rows[1], 'typeCode': rows[2], 'TypeCodeDescription': rows[3], 'LayerDescription': rows[4], 'ProjectionDate': rows[5], 'RCP': rows[6]} for rows in reader}
	return mydict

def newOrOldFiles():
	'''Upload new data or load the past pickle files'''
	#THINGS THAT CHANGE
	#####################################
	#Add values to to the index
	#If you rerun increase this number to avoid unique id collisions
	uniqid = passwordSetAndUqiValue()
	######################################

	#Set the algorithm to be used niche model(s)
	alg = cl.sdm.getAlgorithmFromCode('ATT_MAXENT')
	alg.setParameter('threshold', 0)

	whilePostLayers = True
	while whilePostLayers:
		inputType = raw_input('Rerun post TYPECODES and post LAYERS or use a past run pickle IDs ("new" or "old"): ')
		if inputType.lower() == 'new':
			postDicLayers = rawMetaData()

			postTypeCode(postDicLayers)
			postDicLayers = postLayers(postDicLayers)
			whilePostLayers = False
		elif inputType.lower() == 'old':
			postDicLayers = pickleFilesLayersAndOccurr()
			whilePostLayers = False
		else:
			whilePostLayers = True

	whileOccurrence = True
	while whileOccurrence:
		inputOccurrence = raw_input('Rerun post OCCURRENCE or use a past run pickle IDs ("new" or "old"): ')
		if inputOccurrence.lower() == 'new':
			occurs = postOccurrence()
			whileOccurrence = False
		elif inputOccurrence.lower() == 'old':
			occurs = pickleFileOccurrence()
			whileOccurrence = False
		else:
			whileOccurrence = True

	whileScenario = True
	while whileScenario:
		inputScenario = raw_input('Rerun post SCENARIO or use a past run pickle IDs ("new" or "old"): ')
		if inputScenario.lower() == 'new':
			scenarioDic, sceKey = postScenario(postDicLayers, uniqid)
			newPostExperiment(scenarioDic, sceKey, occurs, alg)
			whileScenario = False
		elif inputScenario.lower() == 'old':
			oldPostExperiment(pickleFileScenario(), occurs, alg)
			whileScenario = False
		else:
			whileScenario = True

if __name__ == '__main__':
	main()
