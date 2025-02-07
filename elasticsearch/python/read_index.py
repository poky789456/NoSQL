import warnings
from elasticsearch import Elasticsearch
warnings.filterwarnings('ignore')

import requests
res = requests.get('http://localhost:9200?pretty')

es = Elasticsearch('http://localhost:9200')
res2 = es.search(index="movies", body={"query":{"match_all":{}}})
# print(res2)

res3 = es.search(index="movies", body=
{
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "directors": "Ron"
          }
        },
      ]
    }
  }
})

# print(res3)

res4 = es.search(index="receipe", body={
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "ingredients.name": "parmesan"
          }
        }
      ], 
      "must_not": [
        {
          "match": {
            "ingredients.name": "tuna"
          }
        }
      ], 
      "filter": [
        {
          "range":{
            "preparation_time_minutes": {
              "lte":15
            }
          }
        }
        ]
    }
  }
})
# print(res4)


# Chercher par prefix 

res_prefix = es.search(index="cities", body={"query": {"prefix" : { "city" : "l" }}})
# print(res_prefix)

#agregation simple -> movies/years
res5 = es.search(index="movies",body={"aggs" : {
    "nb_par_annee" : {
        "terms" : {"field" : "year"}
}}})

print(res5['aggregations'])