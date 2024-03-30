from typing import Set
import os
# from langchain_google_vertexai import VertexAIEmbeddings
from generic_helper import config_helper
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
REGION = config_helper.get_config_value ("GENERAL", "region_ds")
COLLECTION_NAME = "text_tableembed"
PATH = config_helper.get_config_value ("COLLECTION", f"{COLLECTION_NAME}")
 

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

        sourceImage = f"{PATH}/images/{bq_similarity.similarity_search(BQ_PROJECT_ID, BQ_DS_NAME, COLLECTION_NAME, prompt, 1 )}"
        generated_response = multimodal_infer.get_response_from_image(prompt, sourceImage)

        
        # generated_response = rag_pgvector.run_llm(
        #         pgvector_retrieval = pgvector_retrieval,
        #         query=prompt, chat_history=st.session_state["chat_history"]
        #         )
        

        # sources = set(
        #     [os.path.basename(doc.metadata["source"]) for doc in generated_response["source_documents"]]
        # )
        # formatted_response = (
        #     f"{generated_response['result']} \n {create_sources_string(sources)}"
        # )

        # st.session_state.chat_history.append((prompt, generated_response["result"]))
        # st.session_state.user_prompt_history.append(prompt)
        # st.session_state.chat_answers_history.append(formatted_response)

# if st.session_state["chat_answers_history"]:
#     for generated_response, user_query in zip(
#         st.session_state["chat_answers_history"],
#         st.session_state["user_prompt_history"],
#     ):
    # message(
    #     prompt,
    #     is_user=True,
    # )
    message(f"{generated_response}")
    st.header = f"source: {sourceImage}"
