from neo4j import GraphDatabase


driver = GraphDatabase.driver("neo4j+s://id.databases.neo4j.io", auth=("neo4j", "password"))

driver.verify_connectivity()
from langchain_core.documents import Document

def query_graph(entities):
    docs = []

    with driver.session() as session:
        for ent, label, sentence in entities:
            result = session.run(
                "MERGE (e:Entity {name: $name, label: $label}) "
                "RETURN e.name AS name, e.label AS label",
                name=ent,
                label=label
            )
            record = result.single()
            if record:
                # name = record["name"]
                # label = record["label"]
                content = sentence
                docs.append(Document(page_content=content))

    print("Docs************************", docs)
    return docs
    


# def create_graph(entities):
#     with driver.session() as session:
#         driver.verify_connectivity()
#         for ent, label in entities:
#             session.run("MERGE (e:Entity {name: $name, label: $label})", name=ent, label=label)