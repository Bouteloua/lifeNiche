from lifemapper.lmClientLib import LMClient
cl = LMClient(userId='321', pwd='Map123')
tc = cl.sdm.postTypeCode('bio19', title='My Type Code', description='A simple example layer type code')
tc = cl.sdm.postTypeCode('t_sand', title='My Type Code', description='A simple example layer type code')
tc = cl.sdm.postTypeCode('pc1', title='My Type Code', description='A simple example layer type code')
tc = cl.sdm.postTypeCode('mean', title='My Type Code', description='A simple example layer type code')

cl.sdm.postLayer(name='clim.current.bio19', epsgCode=4326, envLayerType='bio19', units='dd', dataFormat='GTiff', fileName='clim.current.bio19.tif')
cl.sdm.postLayer(name='env.gmted2010.mean', epsgCode=4326, envLayerType='mean', units='dd', dataFormat='GTiff', fileName='env.gmted2010.mean.tif')
cl.sdm.postLayer(name='env.hwsd.t_sand', epsgCode=4326, envLayerType='t_sand', units='dd', dataFormat='GTiff', fileName='env.hwsd.t_sand.tif')
cl.sdm.postLayer(name='spat.dist.pc1', epsgCode=4326, envLayerType='pc1', units='dd', dataFormat='GTiff', fileName='spat.dist.pc1.tif')

occ = cl.sdm.postOccurrenceSet('MyPoints', 'shapefile', 'Caede.shp')

scn = cl.sdm.postScenario([6013, 6014, 6015, 6016], 'myScn', 4326, 'dd', title='My Scenario', resolution=30)

alg = cl.sdm.getAlgorithmFromCode('ATT_MAXENT')

alg.setParameter('threshold', 0)

exp = cl.sdm.postExperiment(alg, 1195, 5665024, prjScns=[1195])


#My input
#TYPECODE #########################################################3
tc = cl.sdm.postTypeCode(code=bio19)
tc = cl.sdm.postTypeCode(code=t_sand)
tc = cl.sdm.postTypeCode(code=pc1)
tc = cl.sdm.postTypeCode(code=mean)

cl.sdm.postLayer(name=clim.current.bio19, epsgCode=4326, envLayerType=bio19, units=dd, dataFormat=GTiff, fileName=../views/GTiff/clim.current.bio19.tif, title=clim.current.bio19.tif, description=layerNamePrecipitation of Coldest Quarter Current Climate 1960-2000)
cl.sdm.postLayer(name=env.hwsd.t_sand, epsgCode=4326, envLayerType=t_sand, units=dd, dataFormat=GTiff, fileName=../views/GTiff/env.hwsd.t_sand.tif, title=env.hwsd.t_sand.tif, description=layerNameHarmonized World Soil Database topsoil sand (% frac.))
cl.sdm.postLayer(name=env.gmted2010.mean, epsgCode=4326, envLayerType=mean, units=dd, dataFormat=GTiff, fileName=../views/GTiff/env.gmted2010.mean.tif, title=env.gmted2010.mean.tif, description=layerNameUSGS GMTED2010 Mean Elevation)
cl.sdm.postLayer(name=spat.dist.pc1, epsgCode=4326, envLayerType=pc1, units=dd, dataFormat=GTiff, fileName=../views/GTiff/spat.dist.pc1.tif, title=spat.dist.pc1.tif, description=layerNamePC Axis 1 of Distance Matrix spatial)

cl.sdm.postOccurrenceSet(displayName=Caede, fileType=shapefile, fileName=../views/shapefiles/Caede.shp, epsgCode=4326)

cl.sdm.postScenario(layers=['6009', '6010', '6012', '6011'], code=Scenarioa91_current, epsgCode=4326, units=dd, title=currentClimate Scenario, author=CGW, resolution=30)

cl.sdm.postExperiment(algorithm=<lifemapper.sdm.Algorithm object at 0x7f3cea77fcd0>, mdlScn=1194, occSetId=5665023, prjScns=['1194'], name=Test Experiment2, description=Test run2)




#########################3

cl.sdm.postLayer(name=clim.current.bio19, epsgCode=4326, envLayerType=bio19, units=dd, dataFormat=GTiff, fileName=../views/GTiff/clim.current.bio19.tif, title=clim.current.bio19.tif, description=layerNamePrecipitation of Coldest Quarter Current Climate 1960-2000)
cl.sdm.postLayer(name=clim.current.bio01, epsgCode=4326, envLayerType=bio01, units=dd, dataFormat=GTiff, fileName=../views/GTiff/clim.current.bio01.tif, title=clim.current.bio01.tif, description=layerNameAnnual Mean Temperature Current Climate 1960-2000)
cl.sdm.postLayer(name=clim.ac4550.bio02, epsgCode=4326, envLayerType=bio02, units=dd, dataFormat=GTiff, fileName=../views/GTiff/clim.ac4550.bio02.tif, title=clim.ac4550.bio02.tif, description=layerNameMean Diurnal Range (Mean of monthly (max temp - min temp)) AC RCP45 2050)
cl.sdm.postLayer(name=clim.ac4550.bio01, epsgCode=4326, envLayerType=bio01, units=dd, dataFormat=GTiff, fileName=../views/GTiff/clim.ac4550.bio01.tif, title=clim.ac4550.bio01.tif, description=layerNameAnnual Mean Temperature AC RCP45 2050)
cl.sdm.postLayer(name=env.hwsd.t_gravel, epsgCode=4326, envLayerType=t_gravel, units=dd, dataFormat=GTiff, fileName=../views/GTiff/env.hwsd.t_gravel.tif, title=env.hwsd.t_gravel.tif, description=layerNameHarmonized World Soil Database topsoil gravel (% vol.))
cl.sdm.postLayer(name=env.hwsd.t_sand, epsgCode=4326, envLayerType=t_sand, units=dd, dataFormat=GTiff, fileName=../views/GTiff/env.hwsd.t_sand.tif, title=env.hwsd.t_sand.tif, description=layerNameHarmonized World Soil Database topsoil sand (% frac.))
cl.sdm.postLayer(name=env.gmted2010.mean, epsgCode=4326, envLayerType=mean, units=dd, dataFormat=GTiff, fileName=../views/GTiff/env.gmted2010.mean.tif, title=env.gmted2010.mean.tif, description=layerNameUSGS GMTED2010 Mean Elevation)
cl.sdm.postLayer(name=spat.dist.pc2, epsgCode=4326, envLayerType=pc2, units=dd, dataFormat=GTiff, fileName=../views/GTiff/spat.dist.pc2.tif, title=spat.dist.pc2.tif, description=layerNamePC Axis 2 of Distance Matrix spatial)
cl.sdm.postLayer(name=spat.dist.pc1, epsgCode=4326, envLayerType=pc1, units=dd, dataFormat=GTiff, fileName=../views/GTiff/spat.dist.pc1.tif, title=spat.dist.pc1.tif, description=layerNamePC Axis 1 of Distance Matrix spatial)


cl.sdm.postScenario(layers=['6025', '6026', '6029', '6030', '6032', '6033', '6031'], code=Scenarioa9.41_current, epsgCode=4326, units=dd, title=currentClimate Scenario, author=CGW, resolution=30)
cl.sdm.postScenario(layers=['6027', '6028', '6029', '6030', '6032', '6033', '6031'], code=Scenarioa9.41_ac4550, epsgCode=4326, units=dd, title=ac4550Climate Scenario, author=CGW, resolution=30)

cl.sdm.postExperiment(algorithm=<lifemapper.sdm.Algorithm object at 0x7f9d5a9d1cd0>, mdlScn=1198, occSetId=5665028, prjScns=['1198', '1197'], name=Test Experiment2, description=Test run2)


{'Caede': {'prjScns': ['1198', '1197'], 'metadataUrl': 'http://lifemapper.org/services/sdm/experiments/1399758', 'speciesName': 'Caede', 'description': 'Test run2', 'statusModTime': '2015-02-25 06:57:50', 'occSetId': '5665028', 'mdlScn': '1198', 'bbox': '(-179.17, 14.5, -52.67, 83.17)', 'id': '1399758', 'modTime': '2015-02-25 06:57:50', 'algorithm': <lifemapper.sdm.Algorithm object at 0x7f9d5a9d1cd0>, 'epsgcode': '4326', 'createTime': '2015-02-25 06:57:50', 'user': '321'}}


##############################################3
cl.sdm.postLayer(name=spat.dist.pc2, epsgCode=4326, envLayerType=pc2, units=dd, dataFormat=GTiff, fileName=../views/GTiff/spat.dist.pc2.tif, title=spat.dist.pc2.tif, description=layerNamePC Axis 2 of Distance Matrix spatial)
cl.sdm.postLayer(name=spat.dist.pc1, epsgCode=4326, envLayerType=pc1, units=dd, dataFormat=GTiff, fileName=../views/GTiff/spat.dist.pc1.tif, title=spat.dist.pc1.tif, description=layerNamePC Axis 1 of Distance Matrix spatial)
cl.sdm.postLayer(name=clim.current.bio19, epsgCode=4326, envLayerType=bio19, units=dd, dataFormat=GTiff, fileName=../views/GTiff/clim.current.bio19.tif, title=clim.current.bio19.tif, description=layerNamePrecipitation of Coldest Quarter Current Climate 1960-2000)
cl.sdm.postLayer(name=clim.current.bio02, epsgCode=4326, envLayerType=bio02, units=dd, dataFormat=GTiff, fileName=../views/GTiff/clim.current.bio02.tif, title=clim.current.bio02.tif, description=layerNameMean Diurnal Range (Mean of monthly (max temp - min temp)) Current Climate 1960-2000)
cl.sdm.postLayer(name=clim.current.bio01, epsgCode=4326, envLayerType=bio01, units=dd, dataFormat=GTiff, fileName=../views/GTiff/clim.current.bio01.tif, title=clim.current.bio01.tif, description=layerNameAnnual Mean Temperature Current Climate 1960-2000)
cl.sdm.postLayer(name=clim.ac4570.bio19, epsgCode=4326, envLayerType=bio19, units=dd, dataFormat=GTiff, fileName=../views/GTiff/clim.ac4570.bio19.tif, title=clim.ac4570.bio19.tif, description=layerNamePrecipitation of Coldest Quarter AC RCP45 2070)
cl.sdm.postLayer(name=clim.ac4570.bio02, epsgCode=4326, envLayerType=bio02, units=dd, dataFormat=GTiff, fileName=../views/GTiff/clim.ac4570.bio02.tif, title=clim.ac4570.bio02.tif, description=layerNameMean Diurnal Range (Mean of monthly (max temp - min temp)) AC RCP45 2070)
cl.sdm.postLayer(name=clim.ac4570.bio01, epsgCode=4326, envLayerType=bio01, units=dd, dataFormat=GTiff, fileName=../views/GTiff/clim.ac4570.bio01.tif, title=clim.ac4570.bio01.tif, description=layerNameAnnual Mean Temperature AC RCP45 2070)
cl.sdm.postLayer(name=env.gmted2010.mean, epsgCode=4326, envLayerType=mean, units=dd, dataFormat=GTiff, fileName=../views/GTiff/env.gmted2010.mean.tif, title=env.gmted2010.mean.tif, description=layerNameUSGS GMTED2010 Mean Elevation)
cl.sdm.postLayer(name=env.hwsd.t_gravel, epsgCode=4326, envLayerType=t_gravel, units=dd, dataFormat=GTiff, fileName=../views/GTiff/env.hwsd.t_gravel.tif, title=env.hwsd.t_gravel.tif, description=layerNameHarmonized World Soil Database topsoil gravel (% vol.))
cl.sdm.postLayer(name=env.hwsd.t_sand, epsgCode=4326, envLayerType=t_sand, units=dd, dataFormat=GTiff, fileName=../views/GTiff/env.hwsd.t_sand.tif, title=env.hwsd.t_sand.tif, description=layerNameHarmonized World Soil Database topsoil sand (% frac.))
cl.sdm.postLayer(name=env.hwsd.t_ece, epsgCode=4326, envLayerType=t_ece, units=dd, dataFormat=GTiff, fileName=../views/GTiff/env.hwsd.t_ece.tif, title=env.hwsd.t_ece.tif, description=layerNameHarmonized World Soil Database topsoil ECE (salinity dS/m))
cl.sdm.postLayer(name=clim.ac4550.bio19, epsgCode=4326, envLayerType=bio19, units=dd, dataFormat=GTiff, fileName=../views/GTiff/clim.ac4550.bio19.tif, title=clim.ac4550.bio19.tif, description=layerNamePrecipitation of Coldest Quarter AC RCP45 2050)
cl.sdm.postLayer(name=clim.ac4550.bio02, epsgCode=4326, envLayerType=bio02, units=dd, dataFormat=GTiff, fileName=../views/GTiff/clim.ac4550.bio02.tif, title=clim.ac4550.bio02.tif, description=layerNameMean Diurnal Range (Mean of monthly (max temp - min temp)) AC RCP45 2050)
cl.sdm.postLayer(name=clim.ac4550.bio01, epsgCode=4326, envLayerType=bio01, units=dd, dataFormat=GTiff, fileName=../views/GTiff/clim.ac4550.bio01.tif, title=clim.ac4550.bio01.tif, description=layerNameAnnual Mean Temperature AC RCP45 2050)


cl.sdm.postScenario(layers=['6044', '6045', '6046', '6051', '6052', '6053', '6042', '6043', '6050'], code=Scenarioa31-current, epsgCode=4326, units=dd, title=currentClimate Scenario, author=CGW, resolution=30)
cl.sdm.postScenario(layers=['6047', '6048', '6049', '6051', '6052', '6053', '6042', '6043', '6050'], code=Scenarioa31-ac4570, epsgCode=4326, units=dd, title=ac4570Climate Scenario, author=CGW, resolution=30)
cl.sdm.postScenario(layers=['6054', '6055', '6056', '6051', '6052', '6053', '6042', '6043', '6050'], code=Scenarioa31-ac4550, epsgCode=4326, units=dd, title=ac4550Climate Scenario, author=CGW, resolution=30)


cl.sdm.postExperiment(algorithm=<lifemapper.sdm.Algorithm object at 0x7f6db675ccd0>, mdlScn=1202, occSetId=5665034, prjScns=['1202', '1200', '1201'], name=Test Experiment2, description=Test run2)
cl.sdm.postExperiment(algorithm=<lifemapper.sdm.Algorithm object at 0x7f6db675ccd0>, mdlScn=1202, occSetId=5665035, prjScns=['1202', '1200', '1201'], name=Test Experiment2, description=Test run2)

cl.sdm.postExperiment(algorithm=<lifemapper.sdm.Algorithm object at 0x7fc2e5bd8cd0>, mdlScn=1206, occSetId=5665034, prjScns=['1208', '1206', '1207'], name=Test Experiment2, description=Test run2)
cl.sdm.postExperiment(algorithm=<lifemapper.sdm.Algorithm object at 0x7fc2e5bd8cd0>, mdlScn=1206, occSetId=5665035, prjScns=['1208', '1206', '1207'], name=Test Experiment2, description=Test run2)


{'Caede': {'prjScns': ['1208', '1206', '1207'], 'metadataUrl': 'http://lifemapper.org/services/sdm/experiments/1399767', 'speciesName': 'Caede', 'description': 'Test run2', 'statusModTime': '2015-02-26 09:38:49', 'occSetId': '5665034', 'mdlScn': '1206', 'bbox': '(-179.13, 14.53, -52.67, 83.11)', 'id': '1399767', 'modTime': '2015-02-26 09:38:49', 'algorithm': <lifemapper.sdm.Algorithm object at 0x7fc2e5bd8cd0>, 'epsgcode': '4326', 'createTime': '2015-02-26 09:38:49', 'user': 'demo2'}, 'Abies_balsamea': {'prjScns': ['1208', '1206', '1207'], 'metadataUrl': 'http://lifemapper.org/services/sdm/experiments/1399768', 'speciesName': 'Abies_balsamea', 'description': 'Test run2', 'statusModTime': '2015-02-24 15:10:16', 'occSetId': '5665035', 'mdlScn': '1206', 'bbox': '(-179.13, 14.53, -52.67, 83.11)', 'id': '1399768', 'modTime': '2015-02-24 15:10:16', 'algorithm': <lifemapper.sdm.Algorithm object at 0x7fc2e5bd8cd0>, 'epsgcode': '4326', 'createTime': '2015-02-24 15:10:16', 'user': 'demo2'}}


{'Caede': {'prjScns': ['1211', '1209', '1210'], 'metadataUrl': 'http://lifemapper.org/services/sdm/experiments/1399769', 'speciesName': 'Caede', 'description': 'Test run2', 'statusModTime': '2015-02-26 15:50:33', 'occSetId': '5665036', 'mdlScn': '1209', 'bbox': '(-179.17, 14.5, -52.67, 83.17)', 'id': '1399769', 'modTime': '2015-02-26 15:50:33', 'algorithm': <lifemapper.sdm.Algorithm object at 0x7f2840559cd0>, 'epsgcode': '4326', 'createTime': '2015-02-26 15:50:33', 'user': 'demo3'}, 'Abies_balsamea': {'prjScns': ['1211', '1209', '1210'], 'metadataUrl': 'http://lifemapper.org/services/sdm/experiments/1399770', 'speciesName': 'Abies_balsamea', 'description': 'Test run2', 'statusModTime': '2015-02-26 15:55:26', 'occSetId': '5665037', 'mdlScn': '1209', 'bbox': '(-179.17, 14.5, -52.67, 83.17)', 'id': '1399770', 'modTime': '2015-02-26 15:55:26', 'algorithm': <lifemapper.sdm.Algorithm object at 0x7f2840559cd0>, 'epsgcode': '4326', 'createTime': '2015-02-26 15:55:26', 'user': 'demo3'}}


cl.sdm.postScenario(layers=['6044', '6045', '6046', '6051', '6053', '6042'], code=Scenarioa61-current, epsgCode=4326, units=dd, title=currentClimate Scenario, author=CGW, resolution=30)
cl.sdm.postScenario(layers=['6054', '6055', '6056', '6051', '6053', '6042'], code=Scenarioa61-ac4550, epsgCode=4326, units=dd, title=ac4550Climate Scenario, author=CGW, resolution=30)
cl.sdm.postScenario(layers=['6047', '6048', '6049', '6051', '6053', '6042'], code=Scenarioa61-ac4570, epsgCode=4326, units=dd, title=ac4570Climate Scenario, author=CGW, resolution=30)
####### Completed loadup of scenario IDs see file scenario_dict.pickle for input ############
cl.sdm.postExperiment(algorithm=<lifemapper.sdm.Algorithm object at 0x7f38fb375d90>, mdlScn=1215, occSetId=5665034, prjScns=['1216', '1217', '1215'], name=Test Experiment2, description=Test run2)
cl.sdm.postExperiment(algorithm=<lifemapper.sdm.Algorithm object at 0x7f38fb375d90>, mdlScn=1215, occSetId=5665035, prjScns=['1216', '1217', '1215'], name=Test Experiment2, description=Test run2)
####### Completed loadup of Experiment IDs see file expDic.pickle for input ############
{'Caede': {'prjScns': ['1216', '1217', '1215'], 'metadataUrl': 'http://lifemapper.org/services/sdm/experiments/1399773', 'speciesName': 'Caede', 'description': 'Test run2', 'statusModTime': '2015-02-26 15:41:46', 'occSetId': '5665034', 'mdlScn': '1215', 'bbox': '(-179.13, 14.53, 179.75, 83.11)', 'id': '1399773', 'modTime': '2015-02-26 15:41:46', 'algorithm': <lifemapper.sdm.Algorithm object at 0x7f38fb375d90>, 'epsgcode': '4326', 'createTime': '2015-02-26 15:41:46', 'user': 'demo2'}, 'Abies_balsamea': {'prjScns': ['1216', '1217', '1215'], 'metadataUrl': 'http://lifemapper.org/services/sdm/experiments/1399774', 'speciesName': 'Abies_balsamea', 'description': 'Test run2', 'statusModTime': '2015-02-26 16:43:27', 'occSetId': '5665035', 'mdlScn': '1215', 'bbox': '(-179.13, 14.53, 179.75, 83.11)', 'id': '1399774', 'modTime': '2015-02-26 16:43:27', 'algorithm': <lifemapper.sdm.Algorithm object at 0x7f38fb375d90>, 'epsgcode': '4326', 'createTime': '2015-02-26 16:43:27', 'user': 'demo2'}}



cl.sdm.postScenario(layers=['6044', '6045', '6046', '6051', '6053', '6042'], code=Scenarioa61-current, epsgCode=4326, units=dd, title=currentClimate Scenario, author=CGW, resolution=30)
cl.sdm.postScenario(layers=['6054', '6055', '6056', '6051', '6053', '6042'], code=Scenarioa61-ac4550, epsgCode=4326, units=dd, title=ac4550Climate Scenario, author=CGW, resolution=30)
cl.sdm.postScenario(layers=['6047', '6048', '6049', '6051', '6053', '6042'], code=Scenarioa61-ac4570, epsgCode=4326, units=dd, title=ac4570Climate Scenario, author=CGW, resolution=30)
####### Completed loadup of scenario IDs see file scenario_dict.pickle for input ############
cl.sdm.postExperiment(algorithm=<lifemapper.sdm.Algorithm object at 0x7f38fb375d90>, mdlScn=1215, occSetId=5665034, prjScns=['1216', '1217', '1215'], name=Test Experiment2, description=Test run2)
cl.sdm.postExperiment(algorithm=<lifemapper.sdm.Algorithm object at 0x7f38fb375d90>, mdlScn=1215, occSetId=5665035, prjScns=['1216', '1217', '1215'], name=Test Experiment2, description=Test run2)
####### Completed loadup of Experiment IDs see file expDic.pickle for input ############
{'Caede': {'prjScns': ['1216', '1217', '1215'], 'metadataUrl': 'http://lifemapper.org/services/sdm/experiments/1399773', 'speciesName': 'Caede', 'description': 'Test run2', 'statusModTime': '2015-02-26 15:41:46', 'occSetId': '5665034', 'mdlScn': '1215', 'bbox': '(-179.13, 14.53, 179.75, 83.11)', 'id': '1399773', 'modTime': '2015-02-26 15:41:46', 'algorithm': <lifemapper.sdm.Algorithm object at 0x7f38fb375d90>, 'epsgcode': '4326', 'createTime': '2015-02-26 15:41:46', 'user': 'demo2'}, 'Abies_balsamea': {'prjScns': ['1216', '1217', '1215'], 'metadataUrl': 'http://lifemapper.org/services/sdm/experiments/1399774', 'speciesName': 'Abies_balsamea', 'description': 'Test run2', 'statusModTime': '2015-02-26 16:43:27', 'occSetId': '5665035', 'mdlScn': '1215', 'bbox': '(-179.13, 14.53, 179.75, 83.11)', 'id': '1399774', 'modTime': '2015-02-26 16:43:27', 'algorithm': <lifemapper.sdm.Algorithm object at 0x7f38fb375d90>, 'epsgcode': '4326', 'createTime': '2015-02-26 16:43:27', 'user': 'demo2'}}
franzone@work:~/Documents/lifeNiche/controller$ 
