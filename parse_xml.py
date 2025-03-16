#!/usr/bin/env python 

import sys
import os
import json
import unwiki
import xmltodict
from xml.dom.minidom import parse
from io import StringIO
from html.parser import HTMLParser
from unidecode import unidecode
from langdetect import detect

quotesObject = {}

if (len(sys.argv) == 1):
	print("You must specify an input file.")
	sys.exit()
if (len(sys.argv) == 2):
	cutoffArg = 100
	langArg = "en"
if (len(sys.argv) == 3):
	cutoffArg = int(sys.argv[2])
	langArg = "en"
if (len(sys.argv) > 3):
	cutoffArg = int(sys.argv[2])
	langArg = str(sys.argv[3])

def writeQuotes(content):
	global langArg
	global cutoffArg

	quoteList = []
	write = False
	i = 0

	while i < len(content):
		line = content[i]

		if line.startswith('==') and line[2] != "=":
			write = False
		if write and line.startswith('* '):

			cleaned_line = unwiki.loads(line) # Remove wiki markup
			cleaned_line = strip_tags(cleaned_line) # Remove HTML tags
			cleaned_line = unidecode(cleaned_line) # Convert unicode to ASCII
			cleaned_line = cleaned_line.replace("\\'", "") # Remove escaped apostrophes
			cleaned_line = cleaned_line.replace('\"', '') # Remove double quotes
			' '.join(cleaned_line.split()) # Remove extra whitespace
			cleaned_line = cleaned_line[2:] # Remove bullet point

			if ("://" not in cleaned_line and len(cleaned_line) < cutoffArg):
				if (langArg == "all"):
					quoteList.append(cleaned_line)
				elif (detect(cleaned_line) == langArg):
					quoteList.append(cleaned_line)

		if line == '==Quotes==' or line == '== Quotes ==':
			write = True
		i += 1
	
	return quoteList

def handle(_, value):
	global quotesObject
	try:
		quoteList = writeQuotes(str(value['revision']['text']).split('\\n'))
		if len(quoteList) > 0:
			quotesObject[str(value['title'])] = quoteList
	except Exception as e:
		pass
	return True

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

xmltodict.parse(open(str(sys.argv[1]), "rb"), item_depth=2, item_callback=handle)

os.makedirs('data', exist_ok=True)
with open('data/quotes-' + str(cutoffArg) + '-' + str(langArg) + '.json', 'w') as outfile:
	json.dump(quotesObject, outfile, sort_keys=True, indent=4, ensure_ascii=True)