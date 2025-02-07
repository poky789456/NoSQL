import warnings
from elasticsearch import Elasticsearch
warnings.filterwarnings('ignore')

import requests
res = requests.get('http://localhost:9200?pretty')

es = Elasticsearch('http://localhost:9200')

#create : créer un index
es.indices.create(index="first_index",ignore=400)

#verify
#print (es.indices.exists(index="first_index"))

#delete
# print (es.indices.delete(index="first_index", ignore=[400,404]))

#documents to insert in the elasticsearch index "cities"
doc1 = {"city":"New Delhi", "country":"India"}
doc2 = {"city":"London", "country":"England"}
doc3 = {"city":"Los Angeles", "country":"USA"}



#Inserting doc1 in id=1
es.index(index="cities", doc_type="places", id=1, body=doc1)

#Inserting doc2 in id=2
es.index(index="cities", doc_type="places", id=2, body=doc2)

#Inserting doc3 in id=3
es.index(index="cities", doc_type="places", id=3, body=doc3)


res = es.get(index="cities", doc_type="places", id=2)
#print(res["_source"])

#Mapping
#print(es.indices.get_mapping(index='cities'))

res = es.search(index="movies", body={"query":{"match_all":{}}})
#print(res)

# res = es.search(index="movies", body={
#   "_source": {
#     "includes": [
#       "title",
#       "directors"
#     ],
#     "excludes": [
#       "actors",
#       "genres"
#     ]
#   },
#   "query": {
#     "match": {
#       "directors": "Martin"
#     }
#   }
# })

res2 = es.search(index="movies", body=
{
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "directors": "Ron"
          }
        }
      ]
    }
  }
})


# Définition des paramètres de l'index
settings = {
    "settings": {
        "analysis": {
            "tokenizer": {
                "smiley_tokenizer": {
                    "type": "pattern",
                    "pattern": "(:\\)|:\\()"
                }
            },
            "filter": {
                "smiley_filter": {
                    "type": "pattern_replace",
                    "pattern": ":\\)",
                    "replacement": "_content_"
                },
                "triste_filter": {
                    "type": "pattern_replace",
                    "pattern": ":\\(",
                    "replacement": "_triste_"
                }
            },
            "analyzer": {
                "smiley_analyzer": {
                    "tokenizer": "smiley_tokenizer",
                    "filter": ["lowercase", "smiley_filter", "triste_filter"]
                }
            }
        }
    },
    "mappings": {
        "properties": {
            "text": {
                "type": "text",
                "analyzer": "smiley_analyzer"
            }
        }
    }
}

# Créer l'index avec ce mapping
# es.indices.create(index="french", body=settings)


# doc1 = {"text" : "Une phrase en français :) ..."}
# es.index(index="french", id=1, body=doc1)

res_analyze = es.indices.analyze(index="french",body={
  "text" : "Je dois bosser pour mon QCM sinon je vais avoir une sale note :( ..."
})
print(res_analyze)



