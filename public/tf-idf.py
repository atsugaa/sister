import re
import sys
import json
import pickle
import math

#Argumen check
if len(sys.argv) !=11 :
	print ("\n\\Use python \n\t tf-idf.py [data.json] [output]\n")
	sys.exit(1)


#data argumen
riwayat = ['abu-dawud', 'ahmad', 'bukhari', 'darimi', 'ibnu-majah', 'malik', 'muslim', 'nasai', 'tirmidzi']
r = ['Abu Dawud', 'Ahmad', 'Bukhari', 'Darimi', 'Ibnu Majah', 'Malik', 'Muslim', 'Nasai', 'Tirmidzi']
input_list = [sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9]]
output_data = sys.argv[10]

sw = open("stopword.txt").read().split("\n")

# Clean string function
def clean_str(text) :
	text = (text.encode('ascii', 'ignore')).decode("utf-8")
	text = re.sub("&.*?;", "", text)
	text = re.sub(">", "", text)
	text = re.sub("[\]\|\[\@\,\$\%\*\&\\\(\)\":]", "", text)
	text = re.sub("-", " ", text)
	text = re.sub("\.+", "", text)
	text = re.sub("^\s+","" ,text)
	text = text.lower()
	return text

for i in range(len(input_list)):
	df_data={}
	tf_data={}
	idf_data={}
	tf_idf = {}

	with open(input_list[i], encoding='utf-8') as f:
	    content = json.load(f)

	for data in content:
		tf={}
		#clean and list word
		clean_title = clean_str(data['id'])
		list_word = clean_title.split(" ")

		for word in list_word :
			if word in sw:
				continue

			#tf term frequency
			if word in tf :
				tf[word] += 1
			else :
				tf[word] = 1

			#df document frequency
			if word in df_data :
				df_data[word] += 1
			else :
				df_data[word] = 1

		tf_data[data['number']] = tf

	for x in df_data :
	   idf_data[x] = 1 + math.log10(len(tf_data)/df_data[x])
	fl = 1
	for word in df_data:
		list_doc = []
		for data in content:
			tf_value = 0

			if word in tf_data[data['number']] :
				tf_value = tf_data[data['number']][word]

			weight = tf_value * idf_data[word]

			doc = {
				'number' : data['number'],
				'arab' : data['arab'],
				'id' : data['id'],
				'riwayat' : r[i],
				'score' : weight
			}

			if doc['score'] != 0 :
				if doc not in list_doc:
					list_doc.append(doc)
			#print(riwayat[i]+str(data['number']))
		tf_idf[word] = list_doc
		fl+=1
	with open(riwayat[i], 'wb') as file:
		pickle.dump(tf_idf, file)
	print('ok')