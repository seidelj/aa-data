###Pre and Post survey response decoder###

The script will decode responses answers (A, B, C,...etc) to the the string value.

This assumes you have the relevant data files in a directory  ...PROJECTROOT/surveys/raw

You will also need to to set up a postgresql database.  Set your connection params in the model.py, 

This project uses wave1.csv, which should be stored locally in aa-data/surveys/raw

## Running the script ##
	#Follow instructions in parent dir on activating virtual environment
  	#Make sure your command directory is set to this dir
  
	#initialized the tables in the database
	$(venv) python models.py	

	#upload the surveykey.csv file (provided)	
	$(venv) python upload_key.py

	#Run the script to decode the data!
	$(venv) python decodedata.py
	
