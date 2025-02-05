# NoSQL
 ## ElasticSearch
### Installation d'Elasticsearch avec Docker

## Prérequis
Docker installé sur la machine (https://www.docker.com/)

----------

##  Installation d'Elasticsearch en mode single-node

Exécutez la commande suivante dans un terminal pour télécharger et exécuter l'image Docker d'Elasticsearch en mode single-node :

```docker
docker run -p 9200:9200 -p 9300:9300 -d -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.14.0
```

###  Explication des paramètres :

-   `docker run` : Lance un conteneur à partir d'une image.
    
-   `-p 9200:9200` : Expose le port 9200 pour l'accès à Elasticsearch.
    
-   `-p 9300:9300` : Expose le port 9300 pour la communication entre nœuds.
    
-   `-d` : Exécute le conteneur en arrière-plan (mode détaché).
    
-   `-e "discovery.type=single-node"` : Démarre Elasticsearch en mode single-node pour le développement/test.
    
-   `docker.elastic.co/elasticsearch/elasticsearch:7.14.0` : Nom et version de l'image Elasticsearch.
    

----------

##  Vérification du bon fonctionnement

### Vérification de l'état du cluster

Exécutez la commande suivante pour vérifier que le conteneur Elasticsearch fonctionne correctement :

```
curl 0.0.0.0:9200/_cluster/health | jq
```

Résultat attendu :

```
{
  "cluster_name": "docker-cluster",
  "status": "green",
  "number_of_nodes": 1,
  "number_of_data_nodes": 1,
  "active_shards": 1,
  "unassigned_shards": 0
}
```

###  Vérification des nœuds du cluster

```
curl -X GET "http://0.0.0.0:9200/_cat/nodes?v"
```

Cette commande affiche les informations des nœuds actifs dans le cluster Elasticsearch.

----------

##  Mise en place d'une architecture multi-nœuds avec Docker Compose

Créez un fichier `docker-compose.yml` et ajoutez-y la configuration suivante :

```
version: '3'
services:
  es01:
    image: docker.elastic.co/elasticsearch/elasticsearch:7.15.0
    container_name: es01
    environment:
      - node.name=es01
      - node.roles=master
      - cluster.name=es-docker-cluster
      - bootstrap.memory_lock=true
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
      - "discovery.seed_hosts=es02,es03"
      - "cluster.initial_master_nodes=es01,es02,es03"
    ulimits:
      memlock:
        soft: -1
        hard: -1
    volumes:
      - data01:/usr/share/elasticsearch/data
    ports:
      - 9200:9200
    networks:
      - elastic

  es02:
    image: docker.elastic.co/elasticsearch/elasticsearch:7.15.0
    container_name: es02
    environment:
      - node.name=es02
      - node.roles=data
      - cluster.name=es-docker-cluster
      - bootstrap.memory_lock=true
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
      - "discovery.seed_hosts=es01,es03"
      - "cluster.initial_master_nodes=es01,es02,es03"
    ulimits:
      memlock:
        soft: -1
        hard: -1
    volumes:
      - data02:/usr/share/elasticsearch/data
    networks:
      - elastic

  es03:
    image: docker.elastic.co/elasticsearch/elasticsearch:7.15.0
    container_name: es03
    environment:
      - node.name=es03
      - node.roles=ingest
      - cluster.name=es-docker-cluster
      - bootstrap.memory_lock=true
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
      - "discovery.seed_hosts=es01,es02"
      - "cluster.initial_master_nodes=es01,es02,es03"
    ulimits:
      memlock:
        soft: -1
        hard: -1
    volumes:
      - data03:/usr/share/elasticsearch/data
    networks:
      - elastic

volumes:
  data01:
    driver: local
  data02:
    driver: local
  data03:
    driver: local

networks:
  elastic:
    driver: bridge
```

### Lancement du cluster multi-nœuds

Dans le terminal, exécutez :

```
docker-compose up -d
```

Cette commande va démarrer les trois nœuds Elasticsearch dans un cluster.

###  Vérification du cluster multi-nœuds

Exécutez la commande suivante pour vérifier que tous les nœuds sont bien connectés :

```
curl -X GET "http://0.0.0.0:9200/_cat/nodes?v"

```
----------------------------
### Créer un index et y insérer de la data

Ici, on créer un index dans Elasticsearch nommé cities.

    curl -XPUT 'http://localhost:9200/cities' -H 'Content-Type: application/json' -d '
    {
      "settings": {
        "number_of_shards": 2,
        "number_of_replicas": 2
      }
    }'
Ici, on insère des données.
```docker
curl -XPOST 'http://localhost:9200/cities/_doc' -H 'Content-Type: application/json' -d '
{
  "city": "London",
  "country": "England"
}'
```
### Indexation de data dans Elasticsearch
  On utilisera [ces fichiers json](https://gist.github.com/bdallard/16aa2af027696c4ee4d0bb0db017276a) sauf le fichier movies.json qui est invalide.
  On écrit ce script dans un fichier .sh
  ```bash
curl -s -H "Content-Type: application/x-ndjson" -XPOST localhost:9200/receipe/_bulk --data-binary "@receipe.json" &&\
printf "\n✅ Insertion receipe index to elastic node OK ✅ "

curl -s -H "Content-Type: application/x-ndjson" -XPOST localhost:9200/accounts/docs/_bulk --data-binary "@accounts.json"
printf "\n✅ Insertion accounts index to elastic node OK ✅ "

curl -s -H "Content-Type: application/x-ndjson" -XPOST localhost:9200/movies/_bulk --data-binary "@movies.json"
printf "\n✅ Insertion movies index to elastic node OK ✅ "

curl -s -H "Content-Type: application/x-ndjson" -XPOST localhost:9200/products/_bulk --data-binary "@products.json"
printf "\n✅ Insertion products index to elastic node OK ✅ "
```


