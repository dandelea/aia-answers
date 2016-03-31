import json
import os.path

from lxml import etree
from urllib.request import urlopen

def download_graphicdesign():
	string = "abcdefghijklmnopqrstuvwxyz"
	glossary = []
	for char in string:
		response = urlopen('http://www.prepressure.com/printing-dictionary/'+char)
		broken_html = response.read()
		html = etree.HTML(broken_html)
		words = html.find(".//div/..[@class='entry']").findall('.//h3')
		i=0
		for word in words:
			if word.text is not None:
				glossary.append(word.text)
				i+=1
				if i>=10:
					break;

	with open('files/glossary_graphicdesign.json', 'w') as outfile:
		json.dump(glossary, outfile)

def get_graphicdesign():
	file_path = 'files/glossary_graphicdesign.json'
	if not os.path.exists(file_path):
		download_graphicdesign()

	with open(file_path, 'r') as outfile:
		glossary = json.load(outfile)
	return glossary

def download_chemistry():
	glossary = []
	response = urlopen('https://www.shodor.org/unchem/glossary.html')
	broken_html = response.read()
	html = etree.HTML(broken_html)
	divs = html.find(".//dl").findall('.//dt')
	for div in divs:
		word = div.find(".//b")
		if word.text is not None:
			glossary.append(word.text)
	with open('files/glossary_chemistry.json', 'w') as outfile:
		json.dump(glossary, outfile)

def get_chemistry():
	file_path = 'files/glossary_chemistry.json'
	if not os.path.exists(file_path):
		download_chemistry()

	with open(file_path, 'r') as outfile:
		glossary = json.load(outfile)
	return glossary

if __name__ == '__main__':
	get_chemistry()