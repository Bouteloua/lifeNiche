import glob, sys, os, commands, fiona, cPickle, argparse, datetime
import csv as c
import pandas as pd
from agrumentPasser import getArgs
from shapely.geometry import Point, mapping

from lifemapper.lmClientLib import LMClient
#Change to match your lifemapper ID and password
from password import *

def main(argv=None):

	newOrOldFiles()

########################### THIS WILL NEED TO CHANGE #######################################
def passwordSetAndUqiValue():
	'''This is userName and passwords and unique ID'''
	global cl
	#Setup your client ID and password in the file named password.py
	cl = LMClient(userId=userName, pwd=password)
	#Need to be an unique number within accout index
	uniqid = 'bf006'
	return uniqid
############################## POST TYPECODE ############################################
def postTypeCode(postDicLayers):
	'''The "postTypeCode" function allows you to post a new type code to be used for matching environmental layers.
	 This post request can be as simple as just adding a character string identifying it. '''

	#List holding all the unique typecodes from the recurse function recursionTypeCodeID()
	typeCodeList= []
	#Dictionary holding all the IDs that got posted to lifemapper
	#
	recursionTypeCodeID(postDicLayers, typeCodeList)
	#Dictionary holding the unique typecodes
	typeCodeDictionary = dict()

	for typecode in typeCodeList:
		print 'tc = cl.sdm.postTypeCode(code=%s)' % typecode.lower()

		#posting the unique typecode
		tc = cl.sdm.postTypeCode(code=typecode.lower())

		#Creates a typecode dictionary of all the typecode that got uploaded to lifemapper
		typeCodeDictionary.setdefault(typecode, {
		'created_at': datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'),
		})

	#Save a pickle dictionary of all the typecodes
	
	print typeCodeDictionary
	with open('../views/pastPickleDictionaries/' + 'typeCodeDictionary' + '.pickle', 'wb') as f:
		cPickle.dump(typeCodeDictionary, f)

def recursionTypeCodeID(typeCodeDictionary, typeCodeList):
	if type(typeCodeDictionary)==type({}):
		for key in typeCodeDictionary:
			if key == 'typeCode':
				if typeCodeDictionary[key] not in typeCodeList:
					typeCodeList.append(typeCodeDictionary[key])
			else:
				recursionTypeCodeID(typeCodeDictionary[key], typeCodeList)
	return typeCodeList

############################## POST TYPECODE ###########################################
################################# POST LAYERS ##########################################
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
	with open('../views/pastPickleDictionaries/' + 'LayerDictionary.pickle', 'wb') as f:
		cPickle.dump(layerDictionary, f)
	return layerDictionary

############################## END POST LAYERS ##########################################

############################## POST OCCURRENCE ##########################################
def postOccurrence():
	'''The "postOccurrenceSet" function allows you to add a new occurrence set for SDM experiments to the Lifemapper system.
	It takes a name, a file and file type as well as an option parameter for specifying the map
	projection (as an EPSG code) for your occurrence data.'''
	#Checks if text file called taxaList.csv exist and will tranform textial data into shapefile. If not will need to load the shapefiles into the folder called shapefiles
	taxaFileExist = os.path.isfile('../views/layerDescriptions/taxaList.csv')
	if taxaFileExist == True:
		print 'Loading csv file into shapefiles'
		occurrenceDictionary = csvToShapefile()
	else:
		print 'Loading Shapefiles'
		occurrenceDictionary = getShapeFiles()

	for speciesNameKey, occurrenceValue in occurrenceDictionary.iteritems():
		print "cl.sdm.postOccurrenceSet(displayName=%s, fileType=%s, epsgCode=%s)"  % (str(speciesNameKey), 'shapefile', occurrenceValue['epsgCode'])
		occurrenceObj = cl.sdm.postOccurrenceSet(displayName=str(speciesNameKey),
										  fileType='shapefile',
										  epsgCode=occurrenceValue['epsgCode'])

		#Add the occurrence ID from lifemapper to the dictionary
		occurrenceDictionary[speciesNameKey].update({'occurrenceID':occurrenceObj.id})

	#Save a pickle file of the occurrence IDs
	with open('../views/pastPickleDictionaries/' + 'occurrenceDictionary.pickle', 'wb') as f:
		cPickle.dump(occurrenceDictionary, f)

	print '####### Completed loadup of occurrence IDs see file occurrence_dict.pickle for input ############\n'
	return occurrenceDictionary
############################## END POST OCCURRENCE ######################################

############################## POST SCENARIO ############################################
def postScenario(postDicLayers,uniqid):
	'''The "postScenario" function allows you to add a new scenario for creating SDM models and projections to the Lifemapper system.
	You will need to supply a few parameters at a minimum when posting a new scenario. More information about
	these parameters is available in the code documentation.'''

	scenarioDictionary = dict()
	resolution = 0
	units = 0
	epsgCode = 0

	environemntID = []
	spatialID = []
	try:
		for scenarioKey, value in postDicLayers['env'].iteritems():
			for typeCode_key, layerValue in value.iteritems():
				environemntID.append(postDicLayers['env'][scenarioKey][typeCode_key]['lyrID'])
	except:
		print 'No environment layers loaded!!!!!!!!\n\n'
		pass

	try:
		for scenarioKey, value in postDicLayers['spat'].iteritems():
			for typeCode_key, layerValue in value.iteritems():
				spatialID.append(postDicLayers['spat'][scenarioKey][typeCode_key]['lyrID'])
	except:
		print 'No Spatial layers loaded!!!!!!!!\n\n'
		pass
	#Iterate through all the unique layers and group all set scenario into a list
	for bioClimKey, value in postDicLayers.iteritems():
		for scenarioKey, value1 in value.items():
			#reset the climateLayerID list moving to a new group
			climateLayerID = []
			for typeCodeKey, layerName in value1.items():
				#Only add climate data to the list
				if postDicLayers[bioClimKey][scenarioKey][typeCodeKey]['model'] == 'clim' or postDicLayers[bioClimKey][scenarioKey][typeCodeKey]['model'] == 'agclim':
					climateLayerID.append(postDicLayers[bioClimKey][scenarioKey][typeCodeKey]['lyrID'])
					# continue
				#climateLayerID.append(postDicLayers[bioClimKey][scenarioKey][typeCodeKey]['lyrID'])
				resolution = postDicLayers[bioClimKey][scenarioKey][typeCodeKey]['resolution']
				units = postDicLayers[bioClimKey][scenarioKey][typeCodeKey]['units']
				epsgCode = postDicLayers[bioClimKey][scenarioKey][typeCodeKey]['epsgCode']
				model = postDicLayers[bioClimKey][scenarioKey][typeCodeKey]['model']

			#Do not let set variable get posted to the Dictionary
			if scenarioKey == 'dist' or scenarioKey =='hwsd' or scenarioKey == 'gmted2010':
				continue
			uniqueScenarioName = 'Scenario' + uniqid + '-' + scenarioKey

			if uniqueScenarioName.split('-')[1].lower() == 'current':
				currentID = uniqueScenarioName
				print currentID

			scenarioDictionary.setdefault(uniqueScenarioName, {
				# remove the index + X
				'layers': climateLayerID + environemntID + spatialID,
				'code': uniqueScenarioName,
				'epsgCode': epsgCode,
				'units': units,
				'title': 'Climate Scenario' + scenarioKey,
				'author': 'CGW',
				'resolution': resolution,
				'bioclim': scenarioKey,
				'model': model,
				'created_at': datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'),
				})

			print "cl.sdm.postScenario(layers=%s, code=%s, epsgCode=%s, units=%s, title=%s, author=%s, resolution=%s)" % (climateLayerID + environemntID + spatialID, uniqueScenarioName, epsgCode, units, scenarioKey + 'Climate Scenario', "CGW", resolution)
			# Posting each Scenario
			scn = cl.sdm.postScenario(layers=climateLayerID + environemntID + spatialID, code=uniqueScenarioName, epsgCode=epsgCode, units=units, title=scenarioKey + '_Climate Scenario', author="CGW", resolution=resolution)

			scenarioDictionary[uniqueScenarioName].update({'ScenarioID':scn.id})
			#Save a pickle file of the occurrence IDs

	#print postDicLayers
	with open('../views/pastPickleDictionaries/' + 'scenarioDictionary.pickle', 'wb') as f:
		cPickle.dump(scenarioDictionary, f)

	print '####### Completed loadup of scenario IDs see file scenario_dict.pickle for input ############\n'
	return scenarioDictionary, currentID
	print '#############################################################################################\n'
############################## END POST Scenario #########################################

############################## New POST Experiment ########################################
def newPostExperiment(scenarioDic, currentID, occurrences):
	'''The "postExperiment" function allows you to post a new Lifemapper SDM experiment.'''

	#Set the algorithm to be used niche model(s)
	alg = settingMaxent()

	prjScns_input = []
	for key, value in scenarioDic.iteritems():
		prjScns_input.append(value['ScenarioID'])

	expDic = dict()
	print 'Current ID', scenarioDic[currentID]['ScenarioID']
	for key, occurrence in occurrences.iteritems():
		print "cl.sdm.postExperiment(algorithm=%s, mdlScn=%s, occSetId=%s, prjScns=%s, name=%s, description=%s)" % (alg, scenarioDic[currentID]['ScenarioID'], occurrence['occurrenceID'], prjScns_input, 'Test Experiment2', 'Test run2')
		exp = cl.sdm.postExperiment(algorithm=alg,
									mdlScn=scenarioDic[currentID]['ScenarioID'],
									occSetId=occurrence['occurrenceID'],
									prjScns=prjScns_input,
									name='Experiment Name',
									description='Description data')

		expDic.setdefault(key, {
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
			'mdlScn': scenarioDic[currentID]['ScenarioID'],
			'algorithm': alg,
			'occSetId': occurrence['occurrenceID'],
			'created_at': datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'),
			})
	postTime = datetime.datetime.strftime(datetime.datetime.now(), '_%Y-%m-%d|%H:%M:%S')
	with open('../views/pastPickleDictionaries/' + 'experimentDictionary' + postTime + '.pickle', 'wb') as f:
		cPickle.dump(expDic, f)

	print '####### Completed loadup of Experiment IDs see file expDic.pickle for input ############\n'

	print '\n*********ATT_MAXENT setting**********\n'
	for i in alg.parameters:
		print i.__dict__
############################## new END POST Experiment ####################################

def settingMaxent():
	alg = cl.sdm.getAlgorithmFromCode('ATT_MAXENT')
	alg.setParameter('threshold', 0)
	alg.setParameter('jackknife', 1)
	alg.setParameter('removeduplicates', 1)
	alg.setParameter('outputformat', 0)

	return alg


############################## old POST Experiment ########################################
def oldPostExperiment(scenarioDic, occurrences):
	'''The "postExperiment" function allows you to post a new Lifemapper SDM experiment.'''
	#Set the algorithm to be used niche model(s)
	alg = settingMaxent()

	prjScns_input = []
	for key, value in scenarioDic.iteritems():
		prjScns_input.append(value['ScenarioID'])

	currentLayerName = ''
	for keyOfLayerName in scenarioDic:
		Name = keyOfLayerName.split('-')
		if 'current' in Name:
			currentLayerName = keyOfLayerName

	expDic = dict()
	for key, occurrence in occurrences.iteritems():
		print prjScns_input
		print "cl.sdm.postExperiment(algorithm=%s, mdlScn=%s, occSetId=%s, prjScns=%s, name=%s, description=%s)" % (alg, scenarioDic[currentLayerName]['ScenarioID'], occurrence['occurrenceID'], prjScns_input, 'Test Experiment2', 'Test run2')
		exp = cl.sdm.postExperiment(algorithm=alg,
									mdlScn=scenarioDic[currentLayerName]['ScenarioID'],
									occSetId=occurrence['occurrenceID'],
									prjScns=prjScns_input,
									name='Test Experiment2',
									description='Test run2')

		expDic.setdefault(key, {
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
			'created_at': datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'),
			})

	postTime = datetime.datetime.strftime(datetime.datetime.now(), '_%Y-%m-%d|%H:%M:%S')
	with open('../views/pastPickleDictionaries/' + 'experimentDictionary' + postTime +'.pickle', 'wb') as f:
		cPickle.dump(expDic, f)

	print '####### Completed loadup of Experiment IDs see file expDic.pickle for input ############\n'

	print '\n*********ATT_MAXENT setting**********\n'
	for i in alg.parameters:
		print i.__dict__



#Creates the data structures for the layers
def rawMetaData():
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
		print layer
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

def createFolders():
	requiredFolders = ('shapefiles', 'GTiff', 'speciesOccurrenceRecord_CSV', 'pastPickleDictionaries', 'layerDescriptions', 'experimentOutput')
	path = '../views/'
	for folders in requiredFolders:
	#Check if required folders have been created
		try:
			os.stat(path + folders)
		except:
			os.mkdir(path + folders)

############################# START LOAD OLD FILES ######################################
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

def masterOccurrenceDictionary():
	'''Load the pickle file of occurrence'''
	path = '../views/pastPickleDictionaries/.masterOccurrenceDictionary.pickle'
	if os.path.exists(path):
		with open('../views/pastPickleDictionaries/.masterOccurrenceDictionary.pickle') as f:
			occurrenceDictionary = cPickle.load(f)
	else:
		print 'missing file!!!!!', path
		sys.exit()
	return occurrenceDictionary

def pickleFileOccurrence():
	'''Load the pickle file of occurrence'''
	path = '../views/pastPickleDictionaries/occurrenceDictionary.pickle'
	if os.path.exists(path):
		with open('../views/pastPickleDictionaries/occurrenceDictionary.pickle') as f:
			occurrenceDictionary = cPickle.load(f)
	else:
		print 'missing file!!!!!', path
		sys.exit()
	return occurrenceDictionary


def pickleFileScenario():
	'''Load the pickle file of scenario'''
	path = '../views/pastPickleDictionaries/scenarioDictionary.pickle'
	if os.path.exists(path):
		with open('../views/pastPickleDictionaries/scenarioDictionary.pickle') as f:
			scenarioDictionary = cPickle.load(f)
	else:
		print 'missing file!!!!!', path
		sys.exit()
	return scenarioDictionary

############################# END START LOAD OLD FILES ######################################
def updatePickList():

	occPickList = occurrencePickList()
	occurrenceDictionary = masterOccurrenceDictionary()
	pickList = dict([(i, occurrenceDictionary[i]) for i in occPickList if i in occurrenceDictionary])

			#Save a pickle file of the occurrence IDs
	with open('../views/pastPickleDictionaries/' + 'occurrenceDictionary' + '.pickle', 'wb') as f:
		cPickle.dump(pickList, f)

	print '\nOccurrence dictionary of %s records updated\n' % len(pickList)

def updateMasterOccurrence():
	perPageTotal = 20000
	epsgCodeL = 4326
	print 'Getting a list no greater than %s occurrences records for all %s "epsg code" occurrences' % (perPageTotal, epsgCodeL)
	occurrenceObjs = cl.sdm.listOccurrenceSets(epsgCode=epsgCodeL, perPage=perPageTotal)

	occurrenceDictionary = dict()
	speciesMetaFile = readOccurrenceMetaData()
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
		cPickle.dump(occurrenceDictionary, f)
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
		print "This could be correct if your doing this for a set purpose to remove layers\n"

	print 'Current total of layers uploaded on lifemapper:', LifeMapperCount
	print 'Current total of layers uploaded on .masterLayerDictionary.pickle file', updateCounter

#Take a csv file and makes returns shapefile for each unique species. Then returns a dictionary name, file path, and will add occurrence ID later
def csvToShapefile():
	'''Take a csv file and creates shapefiles'''
	schema = { 'geometry': 'Point', 'properties': { 'name': 'str:24'} }

	speciesOccurrenceRecord_CSV = '../views/speciesOccurrenceRecord_CSV/'
	shapefiles = '../views/shapefiles'

	#Creates a folder is shapefiles does not exist
	try:
		os.stat(speciesOccurrenceRecord_CSV)
	except:
		os.mkdir(speciesOccurrenceRecord_CSV)

	df = pd.read_csv('../views/layerDescriptions/taxaList.csv')
	uniqueNames = df['taxa'].drop_duplicates()
	for uniqueName in uniqueNames:
		filename = df[(df['taxa']  == uniqueName)]
		filename.to_csv(speciesOccurrenceRecord_CSV + uniqueName + '.csv', index = False)

	#The output to all the individual species text files
	csvPath = speciesOccurrenceRecord_CSV


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

def readOccurrenceMetaData():
	'''Open the the file speciesDistributionmetaData.csv to get all the label meta data that cannot get out of the file name. Return a dictionary'''
	with open('../views/layerDescriptions/speciesDistributionmetaData.csv', mode='r') as infile:
		reader = c.reader(infile)
		mydict = {rows[0].lower(): {'shapefile': rows[1], 'occurencesCount': rows[2], 'downloadedTime': rows[3], 'family': rows[4], 'bonapID': rows[5], 'group': rows[6]} for rows in reader}
	return mydict


def readLayerMetaData():
	'''Open the the file layerMetaData.csv to get all the label meta data that cannot get out of the file name. Return a dictionary'''
	with open('../views/layerDescriptions/layerMetaData.csv', mode='r') as infile:
		reader = c.reader(infile)
		mydict = {rows[0].lower(): {'filterType': rows[1], 'typeCode': rows[2], 'TypeCodeDescription': rows[3], 'LayerDescription': rows[4], 'ProjectionDate': rows[5], 'RCP': rows[6], 'Correlated': rows[7]} for rows in reader}
	return mydict

def removeMetaDataFromDictionary(args, postDicLayers):
	if args.Climate.lower() != 'clim' and args.Climate.lower() != 'agclim':
		print 'You cannot run the model with Climate and Agclimate data, Please remove one'
		sys.exit()
	if args.Climate.lower() != 'clim':
		del postDicLayers['clim']
		print 'Deleting Climate layers'
	if args.Climate.lower() != 'agclim':
		del postDicLayers['agclim']
		print 'Deleting Agclimate layers'
	if args.Environment.lower() == 'del':
		del postDicLayers['env']
		print 'Deleting Environment layers'
	if args.Environment.lower() == 'add':
		if 'env.hwsd.t_cecsoil' in postDicLayers['env']['hwsd']['t_cecsoil'].values():
			temp = postDicLayers['env']['hwsd']['t_cecsoil']['envLayerType']
			del postDicLayers['env']['hwsd']['t_cecsoil']
			print 'Deleting environmental layer', temp, 'because of correlating issues'
	if args.Spatial.lower() == 'del':
		print 'Deleting Spatial layers'
		del postDicLayers['spat']

	return postDicLayers

def ArgsCheck():
	# Create the parser object here and pass it in so script-specific arguments can be added if necessary
	parser = argparse.ArgumentParser()
	# Add script-specific arguments before passing in the parser
	args = getArgs(parser)
	return args


def newOrOldFiles():
	'''Upload new data or load the past pickle files'''
	args = ArgsCheck()

	#Check stats of folders
	createFolders()

	#THINGS THAT CHANGE
	#####################################
	#Add values to to the index
	#If you rerun increase this number to avoid unique id collisions
	uniqid = passwordSetAndUqiValue()
	######################################
	if args.UpdateOccurrences:
		if args.UpdateOccurrences.lower() == 'master':
			print 'Updating the master and picklist dictionary'
			updateMasterOccurrence()
			updatePickList()
		elif args.UpdateOccurrences.lower() == 'picklist':
			print 'Updating only species from the picklist occurrencePickList.csv in the folder layerDescriptions'
			updatePickList()
		else:
			print 'ERROR!!'
			sys.exit()


	if args.CleanUpLayer:
		rawDataDictionary = rawMetaData()
		updateLyrsIDs(rawDataDictionary)
		print '\nCompleted updating .masterLayerDictionary. Quiting now'
		sys.exit()

	whilePostLayers = True
	while whilePostLayers:
		inputType = raw_input('Post new TYPECODES and LAYERS to lifemapper or use a snapshot dictionary IDs ("new" or "past"): ')
		if inputType.lower() == 'new':
			rawDataDictionary = rawMetaData()
			postTypeCode(rawDataDictionary)
			layersdictionary = recursionLayersPost(rawDataDictionary)
			print layersdictionary
			whilePostLayers = False
		elif inputType.lower() == 'past':
			layersdictionary = removeMetaDataFromDictionary(args, pickleFilesLayersAndOccurr())
			whilePostLayers = False
		else:
			whilePostLayers = True

	whileOccurrence = True
	while whileOccurrence:
		inputOccurrence = raw_input('Post new OCCURRENCE to lifemapper or use a past snapshot dictionary IDs ("new" or "past"): ')
		if inputOccurrence.lower() == 'new':
			occurs = postOccurrence()
			whileOccurrence = False
		elif inputOccurrence.lower() == 'past':
			occurs = pickleFileOccurrence()
			whileOccurrence = False
		else:
			whileOccurrence = True

	whileScenario = True
	while whileScenario:
		inputScenario = raw_input('Post new SCENARIO to lifemapper or use a past snapshot dictionary IDs ("new" or "past"): ')
		if inputScenario.lower() == 'new':
			scenarioDic, sceKey = postScenario(layersdictionary, uniqid)
			newPostExperiment(scenarioDic, sceKey, occurs)
			whileScenario = False
		elif inputScenario.lower() == 'past':
			oldPostExperiment(pickleFileScenario(), occurs)
			whileScenario = False
		else:
			whileScenario = True

# Script start
if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
