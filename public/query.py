import re
import sys
import json
import pickle

#Argumen check
if len(sys.argv) != 4 :
	print ("\n\nPenggunaan\n\tquery.py [index] [n] [query]..\n")
	sys.exit(1)

query = sys.argv[3].split(" ")
r = sys.argv[1].split(',')
n = int(sys.argv[2])

list_doc = {}
for ind in r:
	with open(ind, 'rb') as indexdb:
		indexFile = pickle.load(indexdb)

	#query
	for q in query:
		try :
			for doc in indexFile[q]:
				if doc['number'] in list_doc :
					list_doc[doc['number']]['score'] += doc['score']
				else :
					list_doc[doc['number']] = doc
		except :
			continue


#convert to list
list_data=[]
for data in list_doc :
	list_data.append(list_doc[data])


#sorting list descending
count=1;
for data in sorted(list_data, key=lambda k: k['score'], reverse=True):
	y = json.dumps(data)
	print(y)
	if (count == n) :
		break
	count+=1