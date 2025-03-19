from celery import Celery
import pickle
import json
import logging

app = Celery('search_service', broker='redis://172.16.9.60:6379/0', backend='redis://172.16.9.60:6379/0')

# Mengonfigurasi logging
logging.basicConfig(level=logging.DEBUG)
app.conf.task_serializer = 'json'  # atau 'pickle' jika Anda lebih suka menggunakan pickle
app.conf.result_serializer = 'json'
app.conf.worker_pool = 'solo'


@app.task
def search_task(index_files, n, query):
    try:
        query_terms = query.split(" ")
        list_doc = {}

        # Pecah string indeks menjadi daftar
        index_file_list = index_files.split(",")

        # Buka file indeks satu per satu
        for index_path in index_file_list:
            with open(index_path, 'rb') as indexdb:
                indexFile = pickle.load(indexdb)

            # Proses query
            for term in query_terms:
                if term in indexFile:
                    for doc in indexFile[term]:
                        if doc['number'] in list_doc:
                            list_doc[doc['number']]['score'] += doc['score']
                        else:
                            list_doc[doc['number']] = doc

        # Konversi hasil ke list dan sorting
        list_data = sorted(list_doc.values(), key=lambda k: k['score'], reverse=True)

        # Ambil hasil sebanyak `n`
        results = [json.dumps(data) for data in list_data]
        return results
    except Exception as e:
        return []
