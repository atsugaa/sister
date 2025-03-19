import re
import sys
import json
import pickle
import grpc
import service_pb2
import service_pb2_grpc

#Argumen check
if len(sys.argv) != 4 :
	print ("\n\nPenggunaan\n\tstart.py [index] [n] [query]..\n")
	sys.exit(1)

query = sys.argv[3]
index_list = sys.argv[1]
n = int(sys.argv[2])

with grpc.insecure_channel('172.16.9.60:50051') as channel:
    stub = service_pb2_grpc.SearchServiceStub(channel)
    try:
        response = stub.SearchHadis(service_pb2.SearchRequest(
            index_files=index_list,
            n=n,
            query=query
        ))
        for i in response.results:
        	print(i)
    except grpc.RpcError as e:
        print(f"RPC failed: {e.details()}")
        print(f"Status code: {e.code()}")
