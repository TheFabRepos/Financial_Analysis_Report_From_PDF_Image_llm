import streamlit as st

from pdf_engineering import pdf_table_to_img
from generic_helper import filesystem_helper, config_helper, gcs_helper

from llm_infer import multimodal_infer
from streamlit_js_eval import streamlit_js_eval

import json
from embedding_core import bq_embedding
import time
import os


def process_file():
    myButton.empty()
    logtxtbox = st.empty()
    logtxtbox.write("") 
    progressbar = st.progress(0, text = "")

    ### Reading properties from config.ini
    BQ_PROJECT_ID = config_helper.get_config_value ("GENERAL", "project_id")
    BQ_DS_NAME = config_helper.get_config_value ("GENERAL", "bq_ds_name")
    REGION = config_helper.get_config_value ("GENERAL", "region_ds")
    BUCKET_NAME = config_helper.get_config_value ("GENERAL", "cloud_storage")

    with st.spinner(text = f"Searching page(s) with table(s) in {st.session_state.filename_with_extension}..."):
      list_page_table = pdf_table_to_img.list_table_in_pdf_from_file(f"{st.session_state.temp_directory}/{st.session_state.filename_with_extension}")
      logtxtbox.write(f"##### {len(list_page_table)} pages containing tables found in {st.session_state.filename_with_extension}...") 
    progressbar = progressbar.progress(0.25, text = "Page containing tables in PDF file have been found...")

    with st.spinner(text = "Converting pages in PDF files to images..."):
       list_images = pdf_table_to_img.convert_pdf_to_image_from_file(f"{st.session_state.temp_directory}/{st.session_state.filename_with_extension}")
    progressbar.progress(0.5, text = "Pages in PDF file has been converted to images ...")
    
    ### Save the page with table in the PDF files as image ###
    with st.spinner(text = "Convert images of pages with table to jpeg file and upload to GCS..."):
      for count, page in enumerate(list_page_table):
        pdf_table_to_img.convert_ppm_to_file (list_images[page], f"{st.session_state.temp_directory}/images/page_{page}.jpg")
        gcs_helper.upload_file_to_GCS(BUCKET_NAME, f"{st.session_state.collection_name}", f"{st.session_state.temp_directory}/images/page_{page}.jpg")
        progressbar.progress((0.5 + (count/len(list_page_table))*0.25) , text = "Saving tables found in PDF file to jpg...")

    ### Getting the embedding_store to store the vectors
    embedding_store = bq_embedding.create_embedding_collection(BQ_PROJECT_ID, BQ_DS_NAME, st.session_state.collection_name ,REGION)

    ### Extract JSON from the table in images ###
    dir_list:list[str] = os.listdir(f"{st.session_state.temp_directory}/images")
    json_values:list[str] = []
    metadatas:list[str] = []
    
    ### Extract the JSON from the image and embed it
    with st.spinner(text = "Extract json from image and embed it..."):
      for count, file in enumerate(dir_list):
          json_values.append (multimodal_infer.extract_table_to_json_from_image(f"{st.session_state.temp_directory}/images/{file}"))
          
          #metadatas.append (f"{st.session_state.temp_directory}/images/{file}")
          metadatas.append (f"{file}")
          # Calculate and store embedding every 10 inferences (we don't want to risk a OOM)
          if (len(json_values) % 10) == 0 or len(dir_list) == (count+1):
              embedding_store.add_texts(json_values, metadatas=metadatas)
              json_values.clear()
              metadatas.clear ()
          progressbar.progress((0.75 + (count/len(dir_list))*0.25) , text = "Extracting and embedding JSON...")

    ### Write the configuration to config file
    collection_name =config_helper.get_config_value ("COLLECTION", "name")
    if (collection_name is None) or  (st.session_state.collection_name not in collection_name):
        collection_name = f"{st.session_state.collection_name},{collection_name} "
        config_helper.write_config("COLLECTION", "name", collection_name)
    config_helper.write_config("COLLECTION", st.session_state.collection_name, st.session_state.temp_directory)

    # Evertything is success, we celabrate
    st.snow()
    time.sleep(5)

    # This action will reset all the session state at the next reload
    del st.session_state["uploaded_already"]
    st.session_state["PDF_Uploaded"] = f"Last PDF analyzed with success:{st.session_state.filename_with_extension}"
  
    streamlit_js_eval(js_expressions="parent.window.location.reload()")
  

if "PDF_Uploaded" in st.session_state:
  st.sidebar.success(st.session_state["PDF_Uploaded"])

st.write("# Import statement for analysis")
st.write("---")

file_uploader = st.empty()

if 'uploaded_already' not in st.session_state:
         st.session_state.uploaded_already = False
         st.session_state.filename_with_extension = ""
         st.session_state.temp_directory = ""
         st.session_state.collection_name = ""
         st.session_state.buttonClicked = False

uploaded_file = file_uploader.file_uploader("Choose a PDF file", accept_multiple_files=False, type=['pdf'])

if st.session_state.uploaded_already == False:
    if uploaded_file is not None:
        bytes_data = uploaded_file.read()

        print(f"Filename is: {uploaded_file.name}")
        #Extract the file name (with extension but without folder name)
        st.session_state.filename_with_extension = uploaded_file.name
        #Extract the file name (without extension or folder name)
        filename_only = uploaded_file.name.split(".")[0]

        
        # create temp local directory to store teh resulting json file
        st.session_state.temp_directory = filesystem_helper.create_tmp_directory (filename_only)
        print(f"Directory: {st.session_state.temp_directory}")
        with open(f"{st.session_state.temp_directory}/{st.session_state.filename_with_extension}", "wb") as f:
            f.write(bytes_data)
        st.session_state.uploaded_already = True
        file_uploader.empty()
        st.subheader('Uploaded files')
        st.success(f'files uploaded {st.session_state.filename_with_extension}')


if st.session_state.uploaded_already == True:
    file_uploader.empty()
    st.write(f"File {st.session_state.filename_with_extension} uploaded successfully...")
    collection_name_textinput = st.empty()
    collection_name = collection_name_textinput.text_input("Enter the name of the collection.")
    st.session_state.collection_name = collection_name
    st.session_state.buttonClicked = True
    myButton = st.empty()
    myButton.button("Ready to process 📝...", on_click=process_file)
    




