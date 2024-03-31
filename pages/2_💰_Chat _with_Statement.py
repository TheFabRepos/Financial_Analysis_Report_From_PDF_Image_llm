from typing import Set
import os
# from langchain_google_vertexai import VertexAIEmbeddings
from generic_helper import config_helper, gcs_helper
#from retrieve_pgvector import rag_pgvector
from embedding_core import bq_similarity
import streamlit as st
from streamlit_chat import message
from llm_infer import multimodal_infer




def create_sources_string(source_urls: Set[str]) -> str:
    if not source_urls:
        return ""
    sources_list = list(source_urls)
    sources_list.sort()
    sources_string = "sources:\n"
    for i, source in enumerate(sources_list):
        sources_string += f"{i+1}. {source}\n"
    return sources_string

#pgvector_retrieval = rag_pgvector.PG_Vector_RAG(collection_name=st.session_state.choice_collection)
#pgvector_retrieval = rag_pgvector.PG_Vector_RAG(collection_name="Google_2022")

### Getting the embedding_store to query against vector store
BQ_PROJECT_ID = config_helper.get_config_value ("GENERAL", "project_id")
BQ_DS_NAME = config_helper.get_config_value ("GENERAL", "bq_ds_name")
COLLECTION_NAME = "fs_embed"
CLOUD_STORAGE = config_helper.get_config_value("GENERAL", "cloud_storage") 

st.header("Chat with your statement 💰 - Helper Bot")
# if (
#     "chat_answers_history" not in st.session_state
#     and "user_prompt_history" not in st.session_state
#     and "chat_history" not in st.session_state
# ):
#     st.session_state["chat_answers_history"] = []
#     st.session_state["user_prompt_history"] = []
#     st.session_state["chat_history"] = []


prompt = st.text_input("Prompt", placeholder="Enter your message here...") or st.button("Submit")

if prompt:
    with st.spinner("Generating response..."):

        sourceImage = f"gs://{CLOUD_STORAGE}/{COLLECTION_NAME}/{bq_similarity.similarity_search(BQ_PROJECT_ID, BQ_DS_NAME, COLLECTION_NAME, prompt, 1)}"
        generated_response = multimodal_infer.get_response_from_image(prompt, sourceImage)

    message (f"{generated_response}")
    # st.chat_message("assistant", avatar="ℹ️").write(f"source: /n {gcs_helper.get_url_from_file_GCS(COLLECTION_NAME,sourceImage.split('/')[-1])}")
    st.chat_message("assistant", avatar="ℹ️").markdown(f"**Source:** [{sourceImage.split('/')[-1]}]({gcs_helper.get_url_from_file_GCS(COLLECTION_NAME,sourceImage.split('/')[-1])})")