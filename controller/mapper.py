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
	for key, layerNames in postDicLayers.iteritems():
		# postTypeCode(
		# 	code-> The code to use for this new type code [string]
		# 	title-> (optional) A title for this type code [string]
		# 	description -> (optional) An extended description of this type code [string]
		# 	)
		descripNote = 'This is a test run for %s' % key 
		cl.sdm.postTypeCode(code=key, title=key.upper(), description=descripNote)
############################## POST TYPECODE #######################################

############################## POST LAYERS #########################################
		for key1, layerName in layerNames.items():

			# postLayer(
			# 	name[unique] -> The name of the layer, 
			# 	epsgCode -> The EPSG code for the layer, 
			# 	envLayerType -> envLayerType, 
			# 	units -> The cell size units,
			# 	dataFormat -> Indicates what format the data is in,
			# 	fileName -> The full path to the local file to be uploaded
			# 	 )
			lyrObj = cl.sdm.postLayer(name=layerName['Name'], epsgCode=layerName['epsgCode'], envLayerType=layerName['envLayerType'], units=layerName['units'], dataFormat=layerName['dataFormat'], fileName=layerName['fileName'], title=layerName['fullname'])

			#Add the Layer ID from lifemapper to the dictionary 
			postDicLayers[key][layerName['fullname']].update({'lyrID':lyrObj.id})

	print postDicLayers

	#Save a pickle file of the layer IDs 
	with open('../views/pickleDic/' + 'layerName_dict' + '.pickle', 'wb') as f:
		cPickle.dump(postDicLayers, f)

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
	add = 0
	#Returns all the gtiff files in the folder GTiff
	folderFiles = glob.glob('../views/GTiff/*.tif')

	#Check list of NULL
	if not folderFiles:
		print "File list is empty"
		sys.exit(0)


	filenameDic = dict() 

	for index, folderFile in enumerate(folderFiles):
		typeCode = folderFile.split("_")[1][:-4]
		layerName = folderFile.split("/")[3][:-4]
		layer = folderFile.split(".")[3]
		if layer.split("_")[0] == 'CURR':
			filenameDic.setdefault(typeCode, {}).setdefault(layerName, {
				# remove the index + X
				'Name': index + add,
				'epsgCode': '4326',
				'envLayerType': layer,
				'units': 'dd',
				'dataFormat': 'GTiff', 
				'fileName': folderFile,
				'title': folderFile.split("/")[3],
				'fullname': folderFile.split("/")[3][:-4],
				'resolution': 2.5,
				'Current': 1,
				})
		else:	
			filenameDic.setdefault(typeCode, {}).setdefault(layerName, {
				# remove the index + X
				'Name': index + add,
				'epsgCode': '4326',
				'envLayerType': layer,
				'units': 'dd',
				'dataFormat': 'GTiff', 
				'fileName': folderFile,
				'title': folderFile.split("/")[3],
				'fullname': folderFile.split("/")[3][:-4],
				'resolution': 2.5,
				'Current': 0,
				})
	return filenameDic

#Take a csv file and makes returns shapefile for each unique species. Then returns a dictionary name, file path, and will add occurrence ID later 
def csvToShapefile():
	schema = { 'geometry': 'Point', 'properties': { 'name': 'str:24'} }

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

if __name__ == '__main__':
  main()

