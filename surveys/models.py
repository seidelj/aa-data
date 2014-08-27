import sqlalchemy
from sqlalchemy import create_engine, Sequence, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgres://postgres:joseph@localhost/aa_surveys')
Base = declarative_base()
Session = sessionmaker(bind=engine)

class SurveyData(Base):
	__tablename__ = 'surveydata'

	id = Column(Integer, Sequence('surveydata_id_seq'),  primary_key=True)
	userid = Column(String)
	question = Column(String)
	choice_key = Column(String)
	choice_value = Column(String)
	issue_flag = Column(String)

class SurveyKey(Base):
	__tablename__ = 'surveykey'

	id = Column(Integer, Sequence('surveykey_id_seq'), primary_key=True)
	pre_or_post = Column(String)
	question_number = Column(String)
	choice_key = Column(String)
	choice_value = Column(String)
	allow_multiple = Column(String)

Base.metadata.create_all(engine)

