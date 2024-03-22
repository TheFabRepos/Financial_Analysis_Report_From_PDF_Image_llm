import streamlit as st
from generic_helper import config_helper
import os


st.set_page_config(
    page_title="Main Page",
    page_icon="📄",
)


def get_list_collectiom() -> list[str]:
    #Read the collections from config.ini
    collection_name:int =config_helper.get_config_value ("COLLECTION", "name")
    collection_name_list:list[str] = collection_name.split(",")
    # It just remove empty string in the list before returning
    return [i for i in collection_name_list if i]

    # with engine.connect() as db_conn:
    #     results = db_conn.execute(sqlalchemy.text("SELECT name from langchain_pg_collection")).fetchall()
    #     list_pgvector_collection = [res.name for res in results]
    #     return list_pgvector_collection




st.header("Chat with your financial statement")
st.subheader("Please select one collection:")


options = get_list_collectiom()
st.session_state.choice_collection = st.radio("", options)

st.text_input("Your choice:", value=st.session_state.choice_collection, disabled=True)
