#connect to our cluster
from elasticsearch import Elasticsearch
import requests
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

import json
r = requests.get("http://localhost:9200")
index = 'ilugc_archives'
doc_type = "email"
body = '{ "from" : "kumar" }'
doc_id = "test_string_1"
try:
  a = es.index(index, doc_type, doc_id, json.loads(body))
  print str(a)
except:
  e = sys.exc_info()[0]
  print str(e)

