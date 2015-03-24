#Mapper Command Description
**General command line input**


##python mapper.py -c -s -e -family -group -title -corlay
**example:** python mapper.py -c clim -s add -e del -family poaceae -corlay yes


-c - indicate which climate layers to use: 
  * 'clim' - use bioclim climate layers
  *	'agclim' - use agricultural climate layers

-s - indicate whether to use spatial layers:
  * 'add' - includes spatial layers
  * 'del' - removes spatial layers
	 
-e - indicate whether to use environmental layers:
  * 'add' - includes environmental layers
  * 'del' - removes environmental layers

-o - indicate whether pull taxa from pre-existing taxa by list
  *	'picklist' - a list of taxa
  * 'master' - run all taxa, this could be really list
		 
-family - indicates whether pull taxa from pre-existing taxa by family
  * 'family' - a predefined family name e.g., poaceae
	 	  
-group - indicates whether pull taxa from pre-existing taxa by group
  * 'group' - a predefined family name e.g., group1. Requires a intger value
	 	  
-title - indicates whether to include title for a given experiment
  * 'yes' - include a title (prompted later to entire title)
  * 'no' - do not include a title

-corlay - indicates whether to include or remove correlated input layers (correlations must be predefined)
  *  'yes' - removes correlated layers
  *  'no' - includes all layers