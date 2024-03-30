from generic_helper import config_helper, gcs_helper
from embedding_core import bq_embedding
from langchain_community.vectorstores import BigQueryVectorSearch
from langchain_google_vertexai import VertexAIEmbeddings
from langchain.vectorstores.utils import DistanceStrategy
from google.cloud import storage
from llm_infer import multimodal_infer


if __name__== "__main__":

    # storage_client = storage.Client()
    # bucket_client = storage_client.get_bucket ("fab_financial_statement")
    # blob = bucket_client.blob('test_embed/page_102.jpg')
    # blob.upload_from_filename('/home/afabrice/fs_bq_embedding_modal_llm/tmp_2022-alphabet-annual-report_202403282009/images/page_102.jpg')

    # print (storage_client)

    # collection_name:int =config_helper.get_config_value ("COLLECTION", "name")
    # collection_name_list:list[str] = collection_name.split(",")
    # collection_name_list = [i for i in collection_name_list if i]
    # print (collection_name_list)
    # # if (collection_name is None) or  (NAME_COLLECTION not in collection_name):
    #     collection_name = f"{NAME_COLLECTION},{collection_name} "
    #     config_helper.write_config("COLLECTION", "name", collection_name)


    ### Getting the embedding_store to query against vector store
    BQ_PROJECT_ID = config_helper.get_config_value ("GENERAL", "project_id")
    BQ_DS_NAME = config_helper.get_config_value ("GENERAL", "bq_ds_name")
    REGION = config_helper.get_config_value ("GENERAL", "region_ds")
    # If collection already exists it will return a handle to the store
    # embedding_store = bq_embedding.create_embedding_collection(BQ_PROJECT_ID, BQ_DS_NAME, "second_embedding_fab" ,REGION)

    print(multimodal_infer.get_response_from_image2("Revenue 2021", "gs://fab_financial_statement/fs_embed/page_34.jpg"))

    embedding = VertexAIEmbeddings(
        model_name="textembedding-gecko@latest", project=BQ_PROJECT_ID
    )
    
    store = BigQueryVectorSearch(
        project_id=BQ_PROJECT_ID,
        dataset_name=BQ_DS_NAME,
        table_name="text_tableembed",
        location=REGION,
        embedding=embedding,
        distance_strategy=DistanceStrategy.EUCLIDEAN_DISTANCE
    )

    # all_texts = ["Apples and oranges", "Cars and airplanes", "Pineapple", "Train", "Banana"]
    # metadatas = [{"len": len(t)} for t in all_texts]

    # store.add_texts(all_texts, metadatas=metadatas)
    # query = "I'd like a fruit."
    # docs = store.similarity_search(query)
    # print(docs)



    query = "Revenue by Geography in 2021"
    query_vector = embedding.embed_query(query)
    docs = store.similarity_search_by_vector(query_vector)
    # docs = retriever.invoke(query)

    print(docs)





    def __init__(self, collection_name):
        connection_string_pgvector = PGVector.connection_string_from_db_params (
                driver=os.getenv("PGVECTOR_DRIVER", "psycopg2"),
                host=os.getenv("PGVECTOR_HOST"),
                port=int(os.getenv("PGVECTOR_PORT")),
                database=os.getenv("PGVECTOR_DATABASE"),
                user=os.getenv("PGVECTOR_USER"),
                password=os.getenv("PGVECTOR_PASSWORD"),
            )
        embedding_function = VertexAIEmbeddings(model_name=EMBEDDING_MODEL)
        pgvector_search = PGVector(
                collection_name = collection_name,
                connection_string = connection_string_pgvector,
                embedding_function = embedding_function) 
        self.retriever = pgvector_search.as_retriever()