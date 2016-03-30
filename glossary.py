import json
from lxml import etree
from urllib.request import urlopen

def get_graphicdesign():
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
				if i>=5:
					break;

	with open('files/glossary_graphicdesign.json', 'w') as outfile:
		json.dump(glossary, outfile)