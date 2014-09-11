import os, sys
import pandas as pd
from user_agents import parse

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DATA = os.path.join(ROOT_DIR, 'raw')
OUT_DIR = os.path.join(ROOT_DIR, 'out')

COLUMNS_DICT = {
    'browser': u'bmi_browser',
    'version': u'bmi_version', 
    'os': u'bmi_operatingsystem', 
    'resolution': u'bmi_screenresolution', 
    'flash': u'bmi_flashversion', 
    'java': u'bmi_javasupport', 
    'useragent': u'bmi_useragent',
    }

GAMING_CONSOLES = ["playstationvita3.15", "nintendowiiu", ]
DESKTOP_COMPUTERS = [
					"windowsnt5.1", "windowsnt6.0", "windowsnt6.1",
					"intelmacosx10.6", "intelmacosx10_4_11", "intelmacosx10_5_6",
					"intelmacosx10_6_6", "intelmacosx10_6_8",
					]
TABLETS = ['ipad',]
MOBILE = ['ipod', 'iphone', 'windowsphone8.0']

def get_column_levels(data, column):
    dfList = data[column][(data['devicetype'] == 'unknown')].tolist()
    return set(dfList)

# last resort
def check_resolution(listedResolution):
	if listedResolution == "1280x720" or listedResolution == "1366x768":
		return "pc"
	elif listedResolution == "320x219":
		return "mobile"
	else:
		return "unknown"

def check_obvious_systems(listedOs):
	if listedOs.replace(" ","").lower() in DESKTOP_COMPUTERS:
		return (True, "desktop")
	elif listedOs.replace(" ","").lower() in GAMING_CONSOLES:
		return (True, "gaming_console")
	elif listedOs.replace(" ","").lower() in TABLETS:
		return (True, "tablet")
	elif listedOs.replace(" ","").lower() in MOBILE:
		return (True, "mobile")
	else: 
		return (False, "unknown")

def check_useragent_is(ua):
	if ua.is_mobile:
		return "mobile"
	elif ua.is_tablet:
		return "tablet"
	elif ua.is_pc:
		return "pc"
	else:
		return False

def determine_os_type(obs, resolved=False):
	ua_string = str(obs[COLUMNS_DICT['useragent']])	
	user_agent = parse(ua_string)
	check_status = check_useragent_is(user_agent)
	if check_status == False:
		check_status = check_obvious_systems(str(obs[COLUMNS_DICT['os']]))
		if check_status[0] == False:
			return check_resolution(obs[COLUMNS_DICT['resolution']]) 
		else:
			return check_status[1]		
	else:	
		return check_status
             

def main():
	print "Enter a filename"
	filename = raw_input()
	if ".dta" in filename:
		df = pd.read_stata(os.path.join(RAW_DATA, filename))
		# I want to treat these as string values rather than actually missing
	elif ".csv" in filename:
		df = pd.read_csv(os.path.join(RAW_DATA, filename))
		df.columns = [x.lower() for x in df.columns]
		df.fillna("missing")
	else:
		sys.exit("File type not detected or supported.  .csv or .dta accepted")
	deviceList = []
	for i in range(len(df.index)):
		observation = df.loc[i]
		os_type = determine_os_type(observation)
		df.loc[i,'devicetype'] = os_type
	#print df.at[0, 'responseid']
	for x in sorted(get_column_levels(df, COLUMNS_DICT['os'])):
		print "Warning: uknown device type for entries labeled   {}".format(x)
	# To save space I'm only going to write an id variable and the newly created devicetype
	df = df[['responseid', 'devicetype']]
	df.to_stata(os.path.join(OUT_DIR,'{}_devices.dta'.format(filename.replace(".dta","").replace(".csv",""))), write_index=False)

if __name__ == "__main__":
    main()
