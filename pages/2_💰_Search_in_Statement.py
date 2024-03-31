from generic_helper import config_helper, gcs_helper
from embedding_core import bq_similarity
import streamlit as st
from streamlit_chat import message
from llm_infer import multimodal_infer
from global_variable import global_scope

### Getting the embedding_store to query against vector store
BQ_PROJECT_ID = config_helper.get_config_value ("GENERAL", "project_id")
BQ_DS_NAME = config_helper.get_config_value ("GENERAL", "bq_ds_name")
COLLECTION_NAME = global_scope.COLLECTION_NAME
CLOUD_STORAGE = config_helper.get_config_value("GENERAL", "cloud_storage") 

st.header(f"Search in statement 💰 - Collection: {COLLECTION_NAME}")

prompt = st.text_input("Prompt", placeholder="Enter your message here...")

if prompt:
    with st.spinner("Generating response..."):

        sourceImage = f"gs://{CLOUD_STORAGE}/{COLLECTION_NAME}/{bq_similarity.similarity_search(BQ_PROJECT_ID, BQ_DS_NAME, COLLECTION_NAME, prompt, 1)}"
        generated_response = multimodal_infer.get_response_from_image(prompt, sourceImage)

    message (f"{generated_response}")
    st.chat_message("assistant", avatar="ℹ️").markdown(f"**Source:** [{sourceImage.split('/')[-1]}]({gcs_helper.get_url_from_file_GCS(COLLECTION_NAME,sourceImage.split('/')[-1])})")