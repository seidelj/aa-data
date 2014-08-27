###Finds a device type best match for user-agent strings

## First time set-up ##
	# From the projects main dir
	$ virtualenv venv
	$ source venv/bin/activate ## venv\scripts\activate for windows
	$ pip install -r requirements.txt

## After first time set-up ##
	#make sure your virtual environment is active
	$ source venv/bin/activate ## venv\scripts\activate for windows

	$ python determine_os.py
	
	#deactivate your venv and your finished
	$ deactivate
