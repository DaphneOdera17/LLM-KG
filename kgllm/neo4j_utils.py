from py2neo import Graph

def get_people_from_neo4j():
    graph = Graph("bolt://localhost:7687", auth=("neo4j", "06794qwe"))

    nodes = graph.run("MATCH (n:Person) RETURN n.name AS id, n.name AS name, n.age AS age").data()
    edges = graph.run(
        "MATCH (a:Person)-[r]->(b:Person) RETURN a.name AS source, b.name AS target, type(r) AS label").data()

    cy_nodes = [{'data': {'id': node['id'], 'name': node['name'], 'age': node['age']}} for node in nodes]
    cy_edges = [{'data': {'source': edge['source'], 'target': edge['target'], 'label': edge['label']}} for edge in
                edges]

    return {
        'nodes': cy_nodes,
        'edges': cy_edges
    }