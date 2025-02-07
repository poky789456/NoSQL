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
-------
### Kibana
Fichier docker-compose.yml
```yml
version: '2.2'
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:7.11.1
    container_name: elasticsearch
    restart: always
    environment:
      - xpack.security.enabled=false
      - discovery.type=single-node
    ulimits:
      memlock:
        soft: -1
        hard: -1
      nofile:
        soft: 65536
        hard: 65536
    cap_add:
      - IPC_LOCK
    volumes:
      - ./elas1:/usr/share/elasticsearch/data
    ports:
      - 9200:9200
      - 9300:9300
    networks:
      - esnet

  kibana:
    container_name: kibana
    image: docker.elastic.co/kibana/kibana:7.11.1
    restart: always
    ports:
      - 5601:5601
    depends_on:
      - elasticsearch
    networks:
      - esnet

networks:
  esnet:
    driver: bridge
```
Exécuter cette commande dans le fichier elas1 pour avoir les droits :
```bash
chmod 777 elas1
```
Commande pour lancer le docker compose : 
```bash
sudo docker compose up
```
Aller sur le lien : http://localhost:5601/app/dev_tools#/console
Et tester des requêtes.

------
### Logstash
(Ne pas oublier d'installer logstach) :
```bash
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo gpg --dearmor -o /usr/share/keyrings/elastic-keyring.gpg

echo "deb [signed-by=/usr/share/keyrings/elastic-keyring.gpg] https://artifacts.elastic.co/packages/8.x/apt stable main" | sudo tee /etc/apt/sources.list.d/elastic-8.x.list

sudo apt-get update
sudo apt-get install logstash
sudo systemctl start logstash
sudo systemctl enable logstash
```
Créer un dossier elk-csv et aller dedans
Créer un nouveau docker-compose.yml (avec des ports différents si nécessaire) :
```yml
version: "3"
services:
  elasticsearch:
    image: elasticsearch:7.6.2
    container_name: elasticsearch
    hostname: elasticsearch
    restart: always
    environment:
      - "discovery.type=single-node"
    ports:
      - 9201:9200
      - 9301:9300
    networks:
      - dockerelk
    volumes:
      - ./elasticsearch/elasticsearch.yml:/usr/share/elasticsearch/config/elasticsearch.yml
  logstash:
    image: logstash:7.6.2
    container_name: logstash
    hostname: logstash
    ports:
      - 9600:9600
      - 8089:8089
    restart: always
    links:
      - elasticsearch:elasticsearch
    depends_on:
      - elasticsearch
    networks:
      - dockerelk
    volumes:
      - ./logstash/logstash.yml:/usr/share/logstash/config/logstash.yml
      - ./logstash/logstash.conf:/usr/share/logstash/pipeline/logstash.conf

  kibana:
    image: kibana:7.6.2
    container_name: kibana
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
    ports:
      - "5602:5601"
    networks:
      - dockerelk
    depends_on:
      - elasticsearch

networks:
  dockerelk:
    driver: bridge
```
Dans elk-csv, créer un dossier elasticsearch et y mettre un fichier elasticsearch.yml :
```yml
cluster.name: docker-cluster
node.name: docker-node
node.master: true
network.host: 0.0.0.0
```
Dans elk-csv, créer un dossier logstash et y mettre les fichiers logstash.conf et logstash.yml :

logstash.conf :
```conf
input {
	file {
		path => "/usr/share/logstash/external-data/data.csv"
		start_position => "beginning"
		sincedb_path => "/dev/null"

	}	
}
filter {
	csv {

		separator => ","
		columns => ["order_id", "order_date", "customer_name", "product_name", "quantity", "price"]

}

  date {

		match => ["order_date", "yyyy-MM-dd"]
	target => "order_date"
	}
}
output {
	elasticsearch {
		hosts => ["elasticsearch:9201"]
		index => "orders-%{+YYYY.MM.dd}"
	}
}
```

logstash.yml :

```yml
xpack.monitoring.elasticsearch.hosts: [ "http://elasticsearch:9200" ]
```
Exécuter cette commande :
```bash
sudo docker compose exec logstash bin/logstash --config.test_and_exit -f /usr/share/logstash/pipeline/logstash.conf
```
#### Avec de la sample data
Pour cette partie, utiliser [ces datas] (https://gist.github.com/bdallard/d4a3e247e8a739a329fd518c0860f8a8)

Une fois le zip téléchargé, mettre le contenu dans un dossier data dans elk-csv.

Changer logstash.conf en fonction des nouvelles data
```
input {
        file {
                start_position => "beginning"
                path => "/usr/share/logstash/external-data/data.csv"
                sincedb_path => "/dev/null" 
        }
      }
filter {
  csv {
      columns => ["orderId","orderGUID","orderPaymentAmount","orderDate","orderPaymentType","latitude","longitude"]
  }
  mutate{
      remove_field => ["message","host","@timestamp","path","@version"]
  }
  mutate {
      convert => {
    "latitude" => "float"
    "longitude" => "float"
    }
  }
  date {
    match => [ "orderdate", "yyyy-MM-dd HH:mm:ss" ]
    target => "orderdate"
  }
  mutate {
    rename => {
      "latitude" => "[location][lat]"
      "longitude" => "[location][lon]"
    }
  }
}

output {
   elasticsearch {
    hosts => "elasticsearch:9200"
    index => "csv-data"
   }
   stdout{}
}
```

Rajouter cette ligne dans docker compose puis le lancer le yml :
```yml
service:
  ...
  logstash:
    ...
      - ./data/data.csv:/usr/share/logstash/external-data/data.csv
    ...
```
Commande pour tester.
```bash
curl -X GET "0.0.0.0:9200/csv-data/_search?q=*" | jq
```
#### JSON
```
input {
    file {
        start_position => "beginning"
        path => "/usr/share/logstash/external-data/data-json.log"
        sincedb_path => "/dev/null" 
    }
}
filter {
    json {
      source => "message"
    }
    mutate{
      remove_field => ["message","host","@timestamp","path","@version"]
    }
}
output {
   elasticsearch {
    hosts => "elasticsearch:9200"
    index => "your-index-name"
   }
   stdout{}
}
```
```yml
service:
  ...
  logstash:
    ...
      - ./data/data-json.log:/usr/share/logstash/external-data/data-json.log
    ...
```
#### Kibana-Logstash

Architecture :
```
├── data
│   └── apache_logs.txt
├── docker-compose.yml
├── logstash
│   └── logstash.conf
```
Télécharger [Sample Web Server logs](https://raw.githubusercontent.com/elastic/examples/master/Common%20Data%20Formats/apache_logs/apache_logs)
Sauvegarder le fichier en tant que apache_logs.txt

logstash.conf :

    input {
            file {
                    start_position => "beginning"
                    path => "/usr/share/logstash/external-data/data.csv"
                    sincedb_path => "/dev/null" 
            }
          }
    filter {
      csv {
          columns => ["orderId","orderGUID","orderPaymentAmount","orderDate","orderPaymentType","latitude","longitude"]
      }
      mutate{
          remove_field => ["message","host","@timestamp","path","@version"]
      }
      mutate {
          convert => {
        "latitude" => "float"
        "longitude" => "float"
        }
      }
      date {
        match => [ "orderdate", "yyyy-MM-dd HH:mm:ss" ]
        target => "orderdate"
      }
      mutate {
        rename => {
          "latitude" => "[location][lat]"
          "longitude" => "[location][lon]"
        }
      }
    }
    
    output {
       elasticsearch {
        hosts => "elasticsearch:9200"
        index => "csv-data"
       }
       stdout{}
    }
    
docker compose.yml :

```yml 
logstash:
  # ...
  volumes:
    # ...
    - ./web_server_logs/logstash-apache.conf:/usr/share/logstash/pipeline/logstash-apache.conf
    - /data/apache_logs.txt:/apache_logs.txt
  # ...
```
Bien penser à changer les permissions dans le conteneur et sur l'hôte si nécessaire

### Ingérer des données en temps réel
```
├── docker-compose.yml
├── filebeat
│   └── filebeat.yml
├── logs
│   └── python_logs.log
├── logstash
│   └── logstash.conf
└── send_logs.py
```
`Créer un dossier elk-stack

send_logs.py : 
```python
import json
import socket
import time
import random
import os

#sample log messages
sample_logs = [
    {"level": "INFO", "message": "User logged in", "user_id": 1},
    {"level": "DEBUG", "message": "Query executed", "user_id": 3},
]
error_logs = [
    {"level": "ERROR", "message": "Failed to connect to database", "user_id": 2},
    {"level": "ERROR", "message": "Permission denied", "user_id": 4},
]
# local set up 
LOGS_DIR = "./logs"
LOG_FILE = "python_logs.log"

#write log into local file 
def send_log(log):
    if not os.path.exists(LOGS_DIR):
        os.makedirs(LOGS_DIR)

    with open(os.path.join(LOGS_DIR, LOG_FILE), "a") as f:
        f.write(json.dumps(log) + "\n")
        print(f"Sent log: {log}")


def simulate_log_stream():
    while True:
        if random.random() < 0.1:
            log = random.choice(error_logs)
        else:
            log = random.choice(sample_logs)

        send_log(log)
        print(log)
        time.sleep(random.uniform(0.5, 3))

if __name__ == "__main__":
    simulate_log_stream()
     
 docker-compose.yml (penser à changer les ports de la partie gauche)
```yml 
version: '2.2'

services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:7.11.1
    container_name: elasticsearch
    environment:
      - discovery.type=single-node
      - ES_JAVA_OPTS=-Xms1g -Xmx1g
      - xpack.security.http.ssl.enabled=false
      - xpack.security.transport.ssl.enabled=false
      - xpack.security.enabled=false
    ports:
      - "9200:9200"
      - "9300:9300"
    networks:
      - elk

  logstash:
    image: docker.elastic.co/logstash/logstash:7.11.1
    container_name: logstash
    volumes:
      - ./logstash/logstash.conf:/usr/share/logstash/pipeline/logstash.conf
    ports:
      - "5044:5044"
      - "5045:5045"
      - "9600:9600"
    networks:
      - elk
    depends_on:
      - elasticsearch

  kibana:
    image: docker.elastic.co/kibana/kibana:7.11.1
    container_name: kibana
    environment:
    - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
    - ELASTICSEARCH_USERNAME=elastic
    - ELASTICSEARCH_PASSWORD=password
    ports:
      - "5601:5601"
    networks:
      - elk
    depends_on:
      - elasticsearch

  filebeat:
    image: docker.elastic.co/beats/filebeat:7.11.2
    container_name: filebeat
    volumes:
      - ./filebeat/filebeat.yml:/usr/share/filebeat/filebeat.yml
      - ./logs:/logs
    networks:
      - elk
    depends_on:
      - logstash
      - elasticsearch

networks:
  elk:
    driver: bridge
```
filebeat.yml :
```yml 
filebeat.inputs:
- type: log
  enabled: true
  paths:
    - /logs/*.log

output.logstash:
  hosts: ["logstash:5045"]
```
logstash.conf : 

    input {
      beats {
        port => 5045
      }
    }
    
    filter {
      json {
        source => "message"
        target => "log"
      }
    }
    
    output {
      elasticsearch {
        hosts => ["elasticsearch:9200"]
        index => "python-logs-%{+YYYY.MM.dd}"
      }
      stdout {
        codec => rubydebug
      }
    }
Lancer le docker compose
Lancer le python  : python3 send_logs.py
curl http://0.0.0.0:9200 (encore, selon le port d'elasticsearch)
curl http://0.0.0.0:9200/_cat/indices?v (Pour voir si l'index a été crée
Le résultat doit ressembler à ça :
 yellow open   python-logs-2023.03.31          B97uqvZ-Rtqh4FjuKr4Czw   1   1       2817            0    320.3kb        320.3kb
 
###       Visualisation des données en temps réel avec Kibana

####  Créer un Index Pattern dans Kibana

 1. Ouvrir Kibana : Naviguez vers http://localhost:5601 dans votre navigateur.
2. Accéder à Stack Management : Dans la barre latérale gauche, cliquez sur Stack Management > Index Patterns.
3. Créer un nouvel index pattern :
4. Cliquez sur Create index pattern.
5. Entrez python-logs* comme nom d’index.
6. Cliquez sur Next.
7. Sélectionnez @timestamp comme Time Filter field name.
8. Cliquez sur Create index pattern.

#### Explorer les Données dans Discover
Allez dans l’onglet Discover dans le menu Kibana.
Vérifiez que les logs s’affichent correctement.
Modifiez l’intervalle de temps avec l’icône de calendrier en haut à droite.
Rafraîchissez la page pour voir les nouvelles données en temps réel.

#### Créer un Tableau de Bord (Dashboard)
➤ Ajouter un premier graphique
Accédez à Dashboard via le menu latéral gauche.
Cliquez sur + Create panel.
Sélectionnez Aggregation based > Metrics.
Choisissez l’index python-logs* et configurez les options selon les besoins.
Enregistrez le graphique.
➤ Ajouter un diagramme circulaire (Pie Chart)
Allez dans Aggregation based graph > Pie.
Sélectionnez l’index python-logs*.
Configurez les options selon vos préférences.
Sauvegardez et ajoutez-le au tableau de bord.
➤ Créer un graphique en séries temporelles (Time Series)
Accédez à TSVB.
Vérifiez que les logs s’affichent avec un intervalle de 30 secondes.
Créez un nouveau panneau et appliquez des filtres spécifiques si nécessaire.
