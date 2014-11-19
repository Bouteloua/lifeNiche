import glob, sys, os, commands, fiona, cPickle
import csv as c
import pandas as pd
from lifemapper.lmClientLib import LMClient
from shapely.geometry import Point, mapping
#Change to match your lifemapper ID and password
from password import *

def main():
	rawMetaData()
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
			filenameDic.setdefault(typeCode, {}).setdefault(layerName, {
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
			print filenameDic
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

