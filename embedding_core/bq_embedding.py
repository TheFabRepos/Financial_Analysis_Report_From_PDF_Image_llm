from langchain.vectorstores.utils import DistanceStrategy
from langchain_community.vectorstores import BigQueryVectorSearch
from langchain_google_vertexai import VertexAIEmbeddings

def create_embedding_collection(project_id:str, dataset_id:str, collection_name:str, region:str) -> BigQueryVectorSearch:
 
    embedding = VertexAIEmbeddings(
        model_name="textembedding-gecko@latest", project=project_id
    )
    
    store = BigQueryVectorSearch(
        project_id=project_id,
        dataset_name=dataset_id,
        table_name=collection_name,
        location=region,
        embedding=embedding,
        distance_strategy=DistanceStrategy.COSINE
    )

    return store

