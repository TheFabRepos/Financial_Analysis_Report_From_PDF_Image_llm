
from pdf_engineering import pdf_table_to_img
from generic_helper import filesystem_helper
from generic_helper import config_helper
from embedding_core import bq_embedding
from llm_infer import multimodal_infer
import os

# Constants

FILENAME_WITH_FULL_PATH = "test_dir_to_delete/2022-alphabet-annual-report.pdf"
BQ_PROJECT_ID = "testfab-362608"
BQ_DS_NAME = "Embedding_DS"
REGION="EU"


if __name__== "__main__":

    ### Check if collection exists in the config.ini ###
    NAME_COLLECTION = "second_embedding"
    collection_name =config_helper.get_config_value ("COLLECTION", "name")
    if (collection_name is None) or  (NAME_COLLECTION not in collection_name):
        collection_name = f"{NAME_COLLECTION},{collection_name} "
        config_helper.write_config("COLLECTION", "name", collection_name)


    ### Create directory  ###
    file_path_directory = filesystem_helper.create_tmp_directory(filesystem_helper.extract_filename(FILENAME_WITH_FULL_PATH))
    ### Identify pages in the PDF which have tables ### 
    list_page_table:list[int] = pdf_table_to_img.list_table_in_pdf_from_file(FILENAME_WITH_FULL_PATH)
    ### Save the page with table in the PDF files as image ###
    image_from_pdf = pdf_table_to_img.convert_pdf_to_image_from_file(FILENAME_WITH_FULL_PATH)
    for count, page in enumerate(list_page_table):
        pdf_table_to_img.convert_ppm_to_file (image_from_pdf[page], f"{file_path_directory}/images/page_{page}.jpg")

    ### Create embedding store ###
    embedding_store = bq_embedding.create_embedding_collection(BQ_PROJECT_ID, BQ_DS_NAME, NAME_COLLECTION ,REGION)

    ### Extract JSON from the table in images ###
    dir_list:list[str] = os.listdir(f"{file_path_directory}/images")
    #json_values:list[str] = []
    #metadatas:list[str] = []
    for file in dir_list:
        json_values = multimodal_infer.extract_table_to_json_from_image(f"{file_path_directory}/images/{file}")
        embedding_store.add_texts([json_values], metadatas = [f"{file_path_directory}/images/{file}"])
        
    
    







    # all_texts = ["Apples and oranges", "Cars and airplanes", "Pineapple", "Train", "Banana"]
    # metadatas = [{"len": len(t)} for t in all_texts]

    # embedding_store.add_texts(all_texts, metadatas=metadatas)





    # dir_list = os.listdir(file_path_directory)
    # for file in dir_list:
    #     if file.endswith(".ppm"):
    #         os.remove(os.path.join(file_path, file))






    # for count, page in enumerate(list_page_table):
    #     pdf_table_to_img.convert_ppm_to_file (image_from_pdf[page], f"{file_path_directory}/images/page_{page}.jpg")

