import argparse

def getArgs(parser):
	parser.add_argument('-c', '--Climate', required=True, help='Use Climate Clim or Agclim')
	parser.add_argument('-e', '--Environment', required=True, help='Use Environment layers add or del')
	parser.add_argument('-s', '--Spatial', required=True, help='Use Spatial layers add or del')

	args = parser.parse_args()

	if not args.Climate:
		args.Climate = raw_input('Use "Climate" or "Agclim" layers: ')

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


	return args