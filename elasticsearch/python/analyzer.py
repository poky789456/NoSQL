import warnings
from elasticsearch import Elasticsearch
warnings.filterwarnings('ignore')

import requests
res = requests.get('http://localhost:9200?pretty')

es = Elasticsearch('http://localhost:9200')


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
es.indices.create(index="french", body=settings)


doc1 = {"text" : "Une phrase en français :) ..."}
es.index(index="french", id=1, body=doc1)

res_analyze = es.indices.analyze(index="french",body={
  "text" : "Je dois bosser pour mon QCM sinon je vais avoir une sale note :( ..."
})
print(res_analyze)