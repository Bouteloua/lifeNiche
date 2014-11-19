import cPickle

with open('../views/pickleDic/layerName_dict.pickle', 'rb') as f:
    lyrs = cPickle.load(f)

#scn = cl.sdm.postScenario(layers=[4311, 4303], code='presClim1', epsgCode=4326, units='dd', title='Current Climate Scenario', author="CGW", resolution=10)
scenarioDic = dict() 
count = 1
resolution = 0
units = 0
epsgCode = 0
ccount2 = 1
for key, layerNames in lyrs.iteritems():
	hold = []
	for key1, layerName in layerNames.items():
		print key, key1, ccount2
		hold.append(lyrs[key][key1]['lyrID'])
		resolution = lyrs[key][key1]['resolution']
		units = lyrs[key][key1]['units']
		epsgCode = lyrs[key][key1]['epsgCode']

		#print key, key1, lyrs[key][key1]['lyrID']
	ccount2 += 1
	count += 1
	keyDic = 'base' + str(count) + '_' + key
	scenarioDic.setdefault(keyDic, {
		# remove the index + X
		'layers': hold,
		'code': keyDic,
		'epsgCode': epsgCode,
		'units': units,
		'title': 'Climate Scenario ' + key,
		'author': 'CGW',
		'resolution': resolution,

		})
	scenarioDic[keyDic].update({'Helloooo':count})
	#print "layers=%s, code=base%s_%s, epsgCode=%s, units=%s, title='Climate Scenario %s', author='CGW', resolution=%s" % (hold, count, key, epsgCode, units, key, resolution)
	#print hold

print scenarioDic['base3_AC4570']

		# lyrObj = cl.sdm.postLayer(name=layerName['Name'], epsgCode=layerName['epsgCode'], envLayerType=layerName['envLayerType'], units=layerName['units'], dataFormat=layerName['dataFormat'], fileName=layerName['fileName'], title=layerName['title'], description=layerName['layerDescription'])
		# postDicLayers[key][key1].update({'lyrID':lyrObj.id})