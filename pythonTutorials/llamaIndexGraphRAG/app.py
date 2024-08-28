from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, ServiceContext, load_index_from_storage
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.node_parser import SentenceSplitter
from llama_index.llms.groq import Groq
import warnings
import os
from neo4j import GraphDatabase
import spacy

warnings.filterwarnings('ignore')

# ---- NEO4J SETUP ----
neo4j_uri = os.environ["NEO4J_URI"]
neo4j_user = os.environ["NEO4J_USER"]
neo4j_password = os.environ["NEO4J_PASSWORD"]
driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))

# ---- ENVIRONMENT VARIABLES ----
groq_api_key = os.environ["GROQ_API_KEY"]

# ---- PROMPT TEMPLATE ----
prompt_template = """
Use the following pieces of information to answer the user's question.
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context: {context}
Graph Insights: {graph_insights}
Question: {question}

Answer the question and provide additional helpful information,
based on the pieces of information and graph insights, if applicable. Be succinct.

Responses should be properly formatted to be easily read.
"""

# Define the context for your prompt
context = "This directory contains resume of different job candidates for the role of software engineer."

# Data ingestion: load all files from a directory
directory_path = "docs"
reader = SimpleDirectoryReader(input_dir=directory_path)
documents = reader.load_data()

# Load spacy model (you can choose a different model)
nlp = spacy.load("en_core_web_trf")

# Function to extract entities and relationships from documents
def populate_graph(documents, driver, nlp):
    with driver.session() as session:
        for doc in documents:
            doc_text = doc.text  # Assuming each document has a 'text' attribute
            nlp_doc = nlp(doc_text)
            concepts = [ent.text for ent in nlp_doc.ents if ent.label_ == "PRODUCT" or ent.label_ == "PERSON" or ent.label_ == "ORG"]

            for concept in concepts:
                session.run("MERGE (:Concept {name: $concept})", concept=concept)

            for i, concept in enumerate(concepts):
                if i + 1 < len(concepts):
                    next_concept = concepts[i + 1]
                    session.run(
                        """
                        MATCH (c1:Concept {name: $concept}), (c2:Concept {name: $next_concept})
                        MERGE (c1)-[:RELATED_TO]->(c2)
                        """,
                        concept=concept, next_concept=next_concept
                    )

# Populate the Neo4j graph
populate_graph(documents, driver, nlp)

# Split the documents into nodes
text_splitter = SentenceSplitter(chunk_size=1024, chunk_overlap=200)
nodes = text_splitter.get_nodes_from_documents(documents, show_progress=True)

# Set up embedding model and LLM
embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
llm = Groq(model="llama3-70b-8192", api_key=groq_api_key)

# Create service context
service_context = ServiceContext.from_defaults(embed_model=embed_model, llm=llm)

# Create vector store index
vector_index = VectorStoreIndex.from_documents(documents, show_progress=True, service_context=service_context, node_parser=nodes)
vector_index.storage_context.persist(persist_dir="./storage_mini")

# Load the index from storage
storage_context = StorageContext.from_defaults(persist_dir="./storage_mini")
index = load_index_from_storage(storage_context, service_context=service_context)


#Query Enhancement with Neo4j

def get_graph_insights(question):
  with driver.session() as session:
    result = session.run(
         """
            MATCH (c:Concept)
            WHERE toLower(c.name) CONTAINS toLower($question)
            OPTIONAL MATCH (c)-[r:RELATED_TO]->(other:Concept)
            RETURN c.name AS concept, collect(other.name) AS related_concepts
            """,
         question=question
         )
    insights = []
    for record in result:
       insights.append(f"Concept: {record['concept']}, Related Concepts: {', '.join(record['related_concepts'])}")
       return "\n".join(insights) if insights else "No relevant graph insights found."



question = "Give me the name of the front-end developer"
graph_insights = get_graph_insights(question)
query_prompt = prompt_template.format(context=context, graph_insights=graph_insights, question=question)
#Query Engine Setup
query_engine = index.as_query_engine(service_context=service_context)
resp = query_engine.query(query_prompt)
print(resp.response)
