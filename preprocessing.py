import numpy as np

from xml.etree.ElementTree import ElementTree
from lxml import etree

def preprocessing(filepath):
	'''
	Características:
		0. Longitud del texto (Carácteres)
		1. Cantidad de párrafos
		2. Longitud media de frases (Carácteres)
		3. Cantidad de hiperenlaces
		4. Cantidad de imágenes
	'''
	tree = ElementTree()
	tree.parse(filepath)
	root = tree.getroot()
	
	answers = root.findall(".//row[@PostTypeId='2']")
	result = np.zeros(shape=(len(answers), 6))

	i = 0
	for row in answers:
		row = row.attrib

		body = etree.HTML(row['Body'])

		if body is not None:
			body_text = "".join(body.itertext())
			body_paragraphs = [paragraph.replace('\n', '') for paragraph in body_text.split('\n\n') if paragraph]
			body_length = sum([len(par) for par in body_paragraphs])
			body_phrases = [phrase.replace('\n', '') for phrase in body_text.split('.') if phrase]
			body_phrases = [p for p in body_phrases if p]
			avg_char_per_phrase = [len(p) for p in body_phrases if len(p)]
			if len(avg_char_per_phrase):
				avg_char_per_phrase = sum(avg_char_per_phrase) / float(len(avg_char_per_phrase))
			else:
				avg_char_per_phrase = 0
			

			num_links = sum(1 for _ in body.iter(tag='a'))
			num_imgs = sum(1 for _ in body.iter(tag='img'))

			score = int(row['Score'])

			result[i, 0] = body_length
			result[i, 1] = len(body_paragraphs)
			result[i, 2] = avg_char_per_phrase
			result[i, 3] = num_links
			result[i, 4] = num_imgs
			result[i, 5] = score

			print(str(i)+"/"+str(len(answers)), end='\r')
			i+=1
	result = result[:i, :]

	avg = np.mean(result[:, 5])
	result[:,5] = result[:,5]>=avg
	
	return result