#Mapper Command Description
**General command line input**


##python mapper.py -c -s -e -family -group -title -corlay
**example:** python mapper.py -c clim -s add -e del -family poaceae -corlay yes


-c - indicate which climate layers to use [**required**]: 
  * 'clim' - use bioclim climate layers
  *	'agclim' - use agricultural climate layers

-s - indicate whether to use spatial layers [**required**]:
  * 'add' - includes spatial layers
  * 'del' - removes spatial layers
	 
-e - indicate whether to use environmental layers [**required**]:
  * 'add' - includes environmental layers
  * 'del' - removes environmental layers

-o - indicate whether pull taxa from pre-existing taxa by list in the occurrencePickList.csv [**optional**]:
  *	'picklist' - a list of taxa
  * 'master' - run all taxa, this could be a really big list and could flood the servers 
		 
-family - indicates whether pull taxa from pre-existing taxa by family in the speciesDistributionmetaData.csv file [**optional**]:
  * 'family' - a predefined family name e.g., poaceae
	 	  
-group - indicates whether pull taxa from pre-existing taxa by group in the speciesDistributionmetaData.csv file [**optional**]:
  * 'group' - a predefined family name e.g., group1. Requires a intger value [**optional**]:
	 	  
-title - indicates whether to include title for a given experiment [**optional**]:
  * 'yes' - include a title (prompted later to entire title)
  * 'no' - do not include a title

-corlay - indicates whether to include or remove correlated input layers correlations must be predefined in the layerMetaData.csv file [**optional**]:
  *  'yes' - removes correlated layers
  *  'no' - includes all layers