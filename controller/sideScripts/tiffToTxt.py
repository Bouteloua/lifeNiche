import glob, sys, os

def main():
	createFolders()
	'''Creates a dictionary off the metadata in the filename of the GTiff'''
	folderFiles = glob.glob('../../views/GTiff/*.tif')

	for folderFile in folderFiles:
		print folderFile
		path = 'touch ../../views/BFF_FILES/' + folderFile.split('/')[4] 
		os.system(path)

def createFolders():
	requiredFolders = (['BFF_FILES'])
	path = '../../views/'
	for folders in requiredFolders:
		print folders
	#Check if required folders have been created
		try:
			os.stat(path + folders)
		except:
			os.mkdir(path + folders)

if __name__ == '__main__':
  main()