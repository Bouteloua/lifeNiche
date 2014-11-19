import glob, sys, os, commands, fiona, cPickle
import csv as c
import pandas as pd
from lifemapper.lmClientLib import LMClient
from shapely.geometry import Point, mapping
#Change to match your lifemapper ID and password
from password import *


def main():
	#This is a hello
	#Setup your client ID and password in the file named password.py
	cl = LMClient(userId=userName, pwd=password)

	#Set the algorithm to be used niche model(s)
	alg = cl.sdm.getAlgorithmFromCode('ATT_MAXENT')

	postDicLayers = rawMetaData()

############################## POST TYPECODE #######################################
		# postTypeCode(
		# 	code-> The code to use for this new type code [string]
		# 	title-> (optional) A title for this type code [string]
		# 	description -> (optional) An extended description of this type code [string]
		# 	)
	for typecode in postDicLayers['CURR'].keys():
		cl.sdm.postTypeCode(code=typecode, title=typecode.upper(), description=postDicLayers['CURR'][typecode]['typeCodeDescription'])
############################## POST TYPECODE #######################################


############################## POST LAYERS #########################################
	for key, layerNames in postDicLayers.iteritems():
		for key1, layerName in layerNames.items():
			lyrObj = cl.sdm.postLayer(name=layerName['Name'], epsgCode=layerName['epsgCode'], envLayerType=layerName['envLayerType'], units=layerName['units'], dataFormat=layerName['dataFormat'], fileName=layerName['fileName'], title=layerName['title'], description=layerName['layerDescription'])
			postDicLayers[key][key1].update({'lyrID':lyrObj.id})
	

	#Save a pickle file of the layer IDs 
	with open('../views/pickleDic/' + 'layerName_dict' + '.pickle', 'wb') as f:
		cPickle.dump(postDicLayers, f)

	print '####### Start of the layer ID dictionary ############'
	print postDicLayers

############################## END POST LAYERS ########################################



############################## POST OCCURRENCE ########################################
	occurrenceDic = csvToShapefile()
	for key, value in occurrenceDic.iteritems():
		occObj = cl.sdm.postOccurrenceSet(displayName=str(key), fileType='shapefile', fileName=value['shpPath'], epsgCode=value['epsgCode'])

		#Add the occurrence ID from lifemapper to the dictionary 
		occurrenceDic[key].update({'occID':occObj.id})
	
	#Save a pickle file of the occurrence IDs 
	with open('../views/pickleDic/' + 'occurrence_dict' + '.pickle', 'wb') as f:
		cPickle.dump(occurrenceDic, f)

	print '####### Start of the occurrence ID dictionary ############'
	print occurrenceDic

############################## END POST OCCURRENCE ########################################




############################################# NEED WORK ###################################
# 	#print layerID
# 	lyrs = cl.sdm.listLayers(epsgCode=4326)
# 	#print lyrs
# 	print typeCode
# 	print layerID

# 	OccObj = cl.sdm.postOccurrenceSet(displayName='MyPoints', fileType='shapefile', fileName='files/longlat.shp', epsgCode=4326)
# # The "postExperiment" function allows you to post a new Lifemapper SDM experiment.
# # Example: Post an experiment base on occurrence set 12345, with the modeling scenario 67, and the projection scenarios 67, 68, 69 using the ATT Maximum Entropy algorithm
#2sd
# #exp = cl.sdm.postExperiment(alg, 67, 12345, prjScns=[67, 68, 69])



# 	scn = cl.sdm.postScenario(layers=[3834], code='presClim', epsgCode=4326, units='dd', title='Current Climate Scenario', author="CGW", resolution=10)
# 	scn = cl.sdm.postScenario(layers=[3835], code='futClim', epsgCode=4326, units='dd', title='Future Climate Scenario', author="CGW", resolution=10)

# 	exp = cl.sdm.postExperiment(algorithm=alg, mdlScn=968, occSetId=5645771, prjScns=[968, 969], name='Test Experiment', description='Test Experiment on Cakile and Present and Future Bio1')
############################################################################################

#Creates the data structures for the layers 
def rawMetaData():
	#If you rerun increase this number to avoid unique id collisions  
	add = 577
	#Returns all the gtiff files in the folder GTiff
	folderFiles = glob.glob('../views/GTiff/*.tif')

	#Check list of NULL
	if not folderFiles:
		print "File list is empty"
		sys.exit(0)


	filenameDic = dict() 
	layernMetaData = readFile()
	for index, folderFile in enumerate(folderFiles):
		typeCode = folderFile.split("_")[1][:-4].strip()
		layerName = folderFile.split("/")[3][:-4].strip().lower()
		layer = folderFile.split(".")[3].strip()
		bioclim = layer.split("_")[0].strip()
		title = folderFile.split("/")[3].strip()
		fullname = folderFile.split("/")[3][:-4].strip()
		if layerName in layernMetaData.keys():
			filenameDic.setdefault(bioclim, {}).setdefault(typeCode, {
				# remove the index + X
				'Name': index + add,
				'filterType': layernMetaData[layerName]['filterType'],
				'typeCode': layernMetaData[layerName]['typeCode'],
				'typeCodeDescription': layernMetaData[layerName]['TypeCodeDescription'],
				'projectionDate': layernMetaData[layerName]['ProjectionDate'],
				'layerDescription': layernMetaData[layerName]['LayerDescription'],
				'RCP': layernMetaData[layerName]['RCP'],
				'bioclim': bioclim,
				'epsgCode': '4326',
				'envLayerType': layer,
				'units': 'dd',
				'dataFormat': 'GTiff', 
				'fileName': folderFile,
				'title': title,
				'fullname': fullname,
				'resolution': '2.5',
				})
		else:
			print '**********************************error***************************************'
			print 'Check the layerMetaData.csv file in the masterOccurrenceList folder. MISSING DATA!!!!!!!!'
			sys.exit(0)
	return filenameDic

#Read the file layerMetaData.csv to get all the label meta data that cannot get out of the file name. Retuen a dictionary. 
def readLayerMetaData():
	with open('../views/masterOccurrenceList/layerMetaData.csv', mode='r') as infile:
		reader = c.reader(infile)
		mydict = {rows[0].lower(): {'filterType': rows[1], 'typeCode': rows[2], 'TypeCodeDescription': rows[3], 'LayerDescription': rows[4], 'ProjectionDate': rows[5], 'RCP': rows[6]} for rows in reader}
	return mydict

#Take a csv file and makes returns shapefile for each unique species. Then returns a dictionary name, file path, and will add occurrence ID later 
def csvToShapefile():
	schema = { 'geometry': 'Point', 'properties': { 'name': 'str:24'} }

	#Creates a folder is shapefiles does not exist
	try:
		os.stat('../views/individualOccurrenceList')
	except:
		os.mkdir('../views/individualOccurrenceList')

	df = pd.read_csv('../views/masterOccurrenceList/longlat.csv')
	uniqueNames = df['Subsp_Ritaxa'].drop_duplicates()
	for uniqueName in uniqueNames:
		filename = df[(df['Subsp_Ritaxa']  == uniqueName)]
		filename.to_csv('../views/individualOccurrenceList/' + uniqueName + '.csv', index = False)

	#The output to all the individual species text files
	csvPath = '../views/individualOccurrenceList/'

	#Creates a folder is shapefiles does not exist
	try:
		os.stat('../views/shapefiles')
	except:
		os.mkdir('../views/shapefiles')

	#The output to all the individual shapefiles
	shpOutBasePath = '../views/shapefiles/'
	#Column name for Longitude
	lonField = 'long'
	#Column name for Latitude
	latField = 'lat'
	#Column name for species names
	nameField = 'Subsp_Ritaxa'

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

def readFile():
	with open('../views/masterOccurrenceList/layerMetaData.csv', mode='r') as infile:
		reader = c.reader(infile)
		mydict = {rows[0].lower(): {'filterType': rows[1], 'typeCode': rows[2], 'TypeCodeDescription': rows[3], 'LayerDescription': rows[4], 'ProjectionDate': rows[5], 'RCP': rows[6]} for rows in reader}
	return mydict

if __name__ == '__main__':
  main()

