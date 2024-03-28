
from google.cloud import bigquery

client = bigquery.Client()

def similarity_search(bq_project_id, bq_ds_name, collection_name, query, k) -> str:
    
    querySimilarity = f"""SELECT base.metadata
        FROM VECTOR_SEARCH
        `{bq_project_id}.{bq_ds_name}.{collection_name}`, 'text_embedding',
        (SELECT ml_generate_embedding_result
        , content AS query
            FROM ML.GENERATE_EMBEDDING(
                MODEL `{bq_project_id}.{bq_ds_name}.geckoembedding`,
                (SELECT '{query}' AS content))
        ), top_k => {k})"""
    query_job = client.query(querySimilarity)
    rows = query_job.result()

    return ''.join([row.metadata for row in rows])



# BQ_PROJECT_ID = config_helper.get_config_value ("GENERAL", "project_id")
# BQ_DS_NAME = config_helper.get_config_value ("GENERAL", "bq_ds_name")
# REGION = config_helper.get_config_value ("GENERAL", "region_ds")