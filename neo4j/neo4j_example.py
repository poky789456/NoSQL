from neo4j import GraphDatabase

uri = "bolt://localhost:7687"

user = "neo4j"
password = "password" # Penser à changer le mot de passe

driver = GraphDatabase.driver(uri, auth=(user, password))

def run_query(query):
    with driver.session() as session:
        result = session.run(query)
        return result.data()

person1 = "CREATE (p:Person {name: 'Alice', age: 30})"
person2 = "CREATE (p:Person {name: 'Bob', age: 25})"
person3 = "CREATE (p:Person {name: 'Charlie', age: 35})"

# run_query(person1)
# run_query(person2)
# run_query(person3)

# Créer des liens (FRIEND)
relationship1 = "MATCH (a:Person {name: 'Alice'}), (b:Person {name: 'Bob'}) CREATE (a)-[:FRIEND]->(b)"
relationship2 = "MATCH (a:Person {name: 'Alice'}), (b:Person {name: 'Charlie'}) CREATE (a)-[:FRIEND]->(b)"
relationship3 = "MATCH (a:Person {name: 'Bob'}), (b:Person {name: 'Charlie'}) CREATE (a)-[:FRIEND]->(b)"

# run_query(relationship1)
# run_query(relationship2)
# run_query(relationship3)

# Trouver toutes les Person
query_all_persons = "MATCH (p:Person) RETURN p.name, p.age"

results = run_query(query_all_persons)
for record in results:
    print(f"Name: {record['p.name']}, Age: {record['p.age']}")


def get_friends(name):
    query = f"MATCH (p:Person {{name: '{name}'}})-[:FRIEND]->(friend) RETURN friend.name, friend.age"
    results = run_query(query)
    return results

name = "Alice"
friends = get_friends(name)

print(f"Friends of {name}:")
for record in friends:
    print(f"Name: {record['friend.name']}, Age: {record['friend.age']}")