import glob, sys, os

def main():
	createFolders()
	'''Creates a dictionary off the metadata in the filename of the GTiff'''
	folderFiles = glob.glob('../../GTiff/*.tif')

	for folderFile in folderFiles:
		path = 'touch ../views/GTiff/' + folderFile.split('/')[3] 
		os.system(path)

def createFolders():
	requiredFolders = ('shapefiles', 'GTiff')
	path = '../views/'
	for folders in requiredFolders:
	#Check if required folders have been created
		try:
			os.stat(path + folders)
		except:
			os.mkdir(path + folders)

if __name__ == '__main__':
  main()