import os
import pandas as pd
from models import Session, SurveyData, SurveyKey

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(SCRIPT_DIR, 'raw')
session = Session()

DF = pd.read_csv(os.path.join(RAW_DIR, 'wave1.csv'), header=0)

# Contains questions as key and whether or not they allow mulitple selection as value
QUESTION_DICT = {}
for value in session.query(SurveyKey).distinct(SurveyKey.question_number, SurveyKey.pre_or_post):
	QUESTION_DICT["{}_question{}".format(value.pre_or_post, value.question_number)] = value.allow_multiple

def get_letter_answers(obs):
	answerListDict = []
	for q, v in QUESTION_DICT.items():
		answerDict = {}
		answerDict[q] = obs[q]
		answerListDict.append(answerDict)
	return answerListDict


def parse_letter_answers(user, answers):
	#answers is listDict where key = questions and value = letter answer
	for a in answers:
		letterAnswer = str(a.values()[0])
		if letterAnswer != "BLANK" and letterAnswer != 'nan':
			answerList = letterAnswer.replace(')',"").replace('(',"").split(',')
			issue_flag = 1 if len(answerList) > 1 and QUESTION_DICT[a.keys()[0]] == '0' else 0
			for v in answerList:
				surveydata = SurveyData(userid=user, question=a.keys()[0], choice_key=v, issue_flag=issue_flag)
				session.add(surveydata)

def decode_answers():
	for instance in session.query(SurveyData).all():
		parsedQuestionField = instance.question.split('_question')
		surveykey = session.query(SurveyKey.choice_value).filter(SurveyKey.choice_key == str(instance.choice_key).lower()).filter(SurveyKey.pre_or_post == str(parsedQuestionField[0])).filter(SurveyKey.question_number == str(parsedQuestionField[1]))
		try:
			instance.choice_value = surveykey.one()
		except:
			print instance.id, instance.choice_key, parsedQuestionField

def main():
	for i in range(len(DF.index)):
		observation = DF.loc[i]
		answers = get_letter_answers(observation)
		parse_letter_answers(observation['userid'], answers)
	decode_answers()
	session.commit()
if __name__ == "__main__":
	main()
