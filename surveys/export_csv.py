import csv, os
from models import Session, SurveyData, Base

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(PROJECT_DIR, 'out')
session = Session()

def main():
	outFile = os.path.join(OUT_DIR, 'surveydata.csv')
	columns = [m.key for m in SurveyData.__table__.columns]
	with open(outFile, 'w+') as csvfile:
		writer = csv.writer(csvfile, csv.excel)
		writer.writerow(columns)
		for obj in session.query(SurveyData):
			objList = []
			for c in columns:
				objList.append(getattr(obj, c))
			writer.writerow(objList)
	

	
if __name__ == "__main__":
	main()

