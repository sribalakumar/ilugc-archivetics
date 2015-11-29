#connect to our cluster
from elasticsearch import Elasticsearch
import requests
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

import json
r = requests.get("http://localhost:9200")
index = 'ilugc_archives'
doc_type = "email"
body = '{ "from" : "kumar" }'
i = "test_string_1"
a = es.index(index='sw', doc_type='people', id=i, body=json.loads(body))
print a

