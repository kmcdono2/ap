#!/usr/bin/env python
# -*- coding=utf-8 -*-

from bs4 import BeautifulSoup
import unicodedata
import csv
import pickle
import regex as re
import pandas as pd
from pandas import *
import numpy as np
from nltk import word_tokenize
from nltk.util import ngrams
import collections
from collections import Counter
import os
import math
from processing_functions import remove_diacritic

date_regex = '(?:([0-9]{4})-([0-9]{1,2})-([0-9]{1,2}))'
text_regex = '(?:([0-9]{1,2}(?:er)?)(?:[ ,.\n\r]+)([A-Za-z\(\) \n\r,.]+)(?:[ ,.\n\r]+)([0-9 ]{4,}))'
month_to_num = {'janvier':'01', 'fevrier':'02', 'mars':'03', 'avril':'04', 'mai':'05', 'juin':'06', 'juillet':'07', 'aout':'08', 'septembre':'09', 'octobre':'10', 'novembre':'11', 'decembre':'12'}
vol_regex = 'Docs\/(vol[0-9]{1,2}).xml'


def parseFiles():
	wrong_dates = set()
	files = os.listdir("Docs/")
	for filename in files:
		if filename.endswith(".xml"):
			print(filename)
			filename = open('Docs/' + filename, "r")
			volno = re.findall(vol_regex, str(filename))[0]
			contents = filename.read()
			soup = BeautifulSoup(contents, 'lxml')
			dates = soup.find_all('date')
			for date in dates:
				if date.attrs:
					coded_date = date['value']
					year, month, day = re.findall(date_regex, coded_date)[0]
					if date.string:
						text_date = remove_diacritic(date.string).decode('utf-8')
					else:
						wrong_dates.add(coded_date + "; " + str(date.contents) + "; " + str(volno) + "\n")
					try:
						text_day, text_month, text_year = re.findall(text_regex, text_date)[0]
						text_month = text_month.lower().replace(' (sic)','').replace('\n','').replace('\r','').replace(' ','')
						text_month = re.sub(r'([ ]{2,})', ' ', text_month)
					except:
						wrong_dates.add(coded_date + "; " + str(date.contents) + "; " + str(volno) + "\n")
					#text_month = remove_diacritic(text_month).decode('utf-8')
					try:
						month_num = month_to_num[text_month]
					except:
						wrong_dates.add(coded_date + "; " + str(date.contents) + "; " + str(volno) + "\n")
					if (month_num != str(month)):
						wrong_dates.add(coded_date + "; " + str(date.contents) + "; " + str(volno) + "\n")
			filename.close()

	file = open('wrong_dates.txt', 'w')
	for item in sorted(wrong_dates):
		file.write(item)
	file.close()


if __name__ == '__main__':
    import sys
    parseFiles()