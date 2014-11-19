import glob, sys, os, commands, fiona, cPickle
import csv as c
import pandas as pd
from lifemapper.lmClientLib import LMClient
from shapely.geometry import Point, mapping
#Change to match your lifemapper ID and password
from password import *

def main():
	postDicLayers = rawMetaData()
	#print postDicLayers
	################GOOD###########################
	# for i in postDicLayers['CURR'].keys():
	# 	print "code=%s, title=%s, description=%s" % (i, i.upper(), postDicLayers['CURR'][i]['typeCodeDescription'])
	################ STOP GOOD###########################
	count = 11
	for key, layerNames in postDicLayers.iteritems():
		for key1, layerName in layerNames.items():
			print "name=%s, epsgCode=%s, envLayerType=%s, units=%s, dataFormat=%s, fileName=%s, title=%s description=%s" %(layerName['Name'], layerName['epsgCode'], layerName['envLayerType'], layerName['units'], layerName['dataFormat'], layerName['fileName'], layerName['title'], layerName['layerDescription'])
			print key1
			postDicLayers[key][key1].update({'lyrID':count})
			#postDicLayers[key][layerName['fullname']
			#postDicLayers[key][layerName['typeCode']].update({'lyrID':count})
			count += 1
	print postDicLayers['CURR']['bio2']
	#"name=layerName['Name'], epsgCode=layerName['epsgCode'], envLayerType=layerName['envLayerType'], units=layerName['units'], dataFormat=layerName['dataFormat'], fileName=layerName['fileName'], title=layerName['fullname']"

	# for key, layerNames in postDicLayers.iteritems():
	#  	print layerNames.keys()
		#cl.sdm.postTypeCode(code=layerName['typeCode'], title=key.upper(), description=descripNote)
	#readFile()
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

def readFile():
	with open('../views/masterOccurrenceList/layerMetaData.csv', mode='r') as infile:
		reader = c.reader(infile)
		mydict = {rows[0].lower(): {'filterType': rows[1], 'typeCode': rows[2], 'TypeCodeDescription': rows[3], 'LayerDescription': rows[4], 'ProjectionDate': rows[5], 'RCP': rows[6]} for rows in reader}
	return mydict

if __name__ == '__main__':
  main()

