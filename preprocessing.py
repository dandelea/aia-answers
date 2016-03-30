import numpy as np
import re
import functions

from xml.etree.ElementTree import ElementTree
from lxml import etree

def preprocessing(filepath, tags, glossary=None):
	'''
	Características:
		0. Longitud del texto (Carácteres)
		1. Cantidad de párrafos
		2. Longitud media de frases (Carácteres)
		3. Cantidad de hiperenlaces
		4. Cantidad de imágenes
		5. Cantidad de términos encontrados en un glosario técnico
	'''
	tree = ElementTree()
	tree.parse(filepath)
	root = tree.getroot()
	
	answers = root.findall(".//row[@PostTypeId='2']")
	result = np.zeros(shape=(len(answers), sum(tags)+1))

	i = 0
	for row in answers:
		row = row.attrib
		body = etree.HTML(row['Body'])

		if body is not None:

			body_text = "".join(body.itertext())
			body_paragraphs = [paragraph.replace('\n', '') for paragraph in body_text.split('\n\n') if paragraph]

			j = 0
			if tags[0]:
				body_length = sum([len(par) for par in body_paragraphs])
				result[i,j] = body_length
				j += 1
			if tags[1]:
				result[i,j] = len(body_paragraphs)
				j += 1
			if tags[2]:
				body_phrases = [phrase.replace('\n', '') for phrase in body_text.split('.') if phrase]
				body_phrases = [p for p in body_phrases if p]
				avg_char_per_phrase = [len(p) for p in body_phrases if len(p)]
				if len(avg_char_per_phrase):
					avg_char_per_phrase = sum(avg_char_per_phrase) / float(len(avg_char_per_phrase))
				else:
					avg_char_per_phrase = 0
				result[i,j] = avg_char_per_phrase
				j += 1
			if tags[3]:
				num_links = sum(1 for _ in body.iter(tag='a'))
				result[i,j] = num_links
				j += 1
			if tags[4]:
				num_imgs = sum(1 for _ in body.iter(tag='img'))
				result[i,j] = num_imgs
				j += 1
			if tags[5]:
				topic_words = 0
				if glossary is not None:
					for word in glossary:
						topic_words += len(re.findall(word, body_text))
				result[i,j] = topic_words
				j += 1

			score = int(row['Score'])
			result[i,j] = score

			#print(str(i)+"/"+str(len(answers)), end='\r')
			i+=1

	result = result[:i, :]

	avg = np.mean(result[:, -1])
	result[:,-1] = result[:,-1]>=avg

	tag_names = []
	if tags[0]:
		tag_names.append('body_length')
	if tags[1]:
		tag_names.append('body_paragraphs')
	if tags[2]:
		tag_names.append('avg_length_phrase')
	if tags[3]:
		tag_names.append('n_links')
	if tags[4]:
		tag_names.append('n_imgs')
	if tags[5]:
		tag_names.append('topic_words')
	
	return result, tag_names