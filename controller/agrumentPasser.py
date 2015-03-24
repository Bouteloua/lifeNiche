import argparse, sys

def getArgs(parser):
	parser.add_argument('-c', '--Climate', required=True, help='Use Climate Clim or Agclim')
	parser.add_argument('-e', '--Environment', required=True, help='Use Environment layers add or del')
	parser.add_argument('-s', '--Spatial', required=True, help='Use Spatial layers add or del')
	parser.add_argument('-o', '--UpdateOccurrences', required=False, help='Create a new "master" or "picklist" dictionary for the occurrences')
	parser.add_argument('-family', '--Family', required=False, help='Select subset of families from past occurrence dictionary')
	parser.add_argument('-group', '--Group', required=False, help='Select an integer batch from past occurrence dictionary')
	parser.add_argument('-cleanlayers', '--CleanUpLayer', required=False, help='Recreate the .masterLayerDictionary ["yes"]')
	parser.add_argument('-corlay', '--Correlatedlayers', required=False, help='Remove highly correlated layers ["yes" or "no"]')
	parser.add_argument('-title', '--Title', required=False, help='Add a title to Post Experiment')

	args = parser.parse_args()
	if args.Title:
		args.Title = str(raw_input('Enter a title name for all the post experiments: '))


	if args.Climate.lower() != 'clim' and args.Climate.lower() != 'agclim':
		print args.Climate.lower()
		ClimateTest = True
		while ClimateTest:
			args.Climate = raw_input('Use "Climate" or "Agclim" layers ["clim or agclim"]: ')
			if args.Climate.lower() == 'clim' or args.Climate.lower() == 'agclim':
				ClimateTest = False
			else:
				ClimateTest = True

	if args.Environment.lower() != 'add' and args.Environment.lower() != 'del':
		environmentTest = True
		while environmentTest:
			args.Environment = raw_input('Include Environment layers: "add" or "del": ')
			if args.Environment.lower() == 'add' or args.Environment.lower() == 'del':
				environmentTest = False
			else:
				environmentTest = True


	if args.Spatial.lower() != 'add' and args.Spatial.lower() != 'del':
		spatialTest = True
		while spatialTest:
			args.Spatial = raw_input('Include Spatial layers: "add" or "del": ')
			if args.Spatial.lower() == 'add' or args.Spatial.lower() == 'del':
				spatialTest = False
			else:
				spatialTest = True


	if args.Family:
		FamilyTest = True
		while FamilyTest:
			if args.Family.lower()[-5:] == 'aceae':
				print 'Selecting family from dictionary', args.Family
				FamilyTest = False
			else:
				args.Family = raw_input('Enter a family name ending with "aceae": ')
				FamilyTest = True

	if args.Group:
		GroupTest = True
		while GroupTest:
			try:
				args.Group = int(args.Group)
			except:
				pass
			if type(args.Group) == type(0):
				print 'Selecting group from dictionary', args.Group
				GroupTest = False

			else:
				args.Group = raw_input('Enter integer to select set batch out of occurrence dictionary: ')
				GroupTest = True

	if args.UpdateOccurrences:
		if args.UpdateOccurrences.lower() != 'master' and args.UpdateOccurrences.lower() != 'picklist':
			updateOccurrencesTest = True
			while updateOccurrencesTest:
				args.UpdateOccurrences = raw_input('Updating the master or picklist dictionary ("master" or "picklist")": ')
				if args.UpdateOccurrences.lower() == 'master' or args.UpdateOccurrences.lower() == 'picklist':
					updateOccurrencesTest = False
				else:
					updateOccurrencesTest = True

	if args.Correlatedlayers:
		if args.Correlatedlayers.lower() != 'yes' and args.Correlatedlayers.lower() != 'no':
			correlatedlayersTest = True
			while correlatedlayersTest:
				args.Correlatedlayers = raw_input('Remove correlated layers "yes" or "no": ')
				if args.Correlatedlayers.lower() == 'yes' or args.Correlatedlayers.lower() == 'no':
					correlatedlayersTest = False
				else:
					correlatedlayersTest = True



	return args
