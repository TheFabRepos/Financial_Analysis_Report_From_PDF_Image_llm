#from langchain_google_vertexai import ChatVertexAI

from generic_helper import config_helper
from vertexai.generative_models import (
    Content,
    GenerationConfig,
    GenerationResponse,
    GenerativeModel,
    Image,
    Part,
)

MULTIMODAL_MODEL = config_helper.get_config_value("GENERAL", "multimodal_model")

# Extract table to json format from the image URI.


def extract_table_to_json_from_image(image_uri:str) -> str:
    """
    Extract table to json format from the image URI.

    Args:
        image_uri: The image URI.

    Returns:
        Json for every table in the image.
    """
    
    model = GenerativeModel(MULTIMODAL_MODEL)
    prompt = "Extract all the possible information for every single table in text format, it's imperative to get year and month to which the extracted data applies to. If the month and year cannot be found in the table directly get the month and year form the text surroundung the table."
    imageContent = Part.from_image(Image.load_from_file(image_uri))

    contents = [
        imageContent,
        prompt,
    ]
    responses = model.generate_content(
        contents,  
        generation_config={
            "max_output_tokens": 2048,
            "temperature": 0,
            "top_p": 1,
            "top_k": 1
            },
        stream=True)
    
    responses = list(responses)
    final_response = ""
    try:
        for response in responses:
            final_response = final_response + response.candidates[0].content.parts[0].text
    except IndexError as e:
        print(f"Exception has occured: {e}")
        return final_response

    return final_response

def get_response_from_image(prompt:str, gcs_uri:str) -> str:
    model = GenerativeModel(MULTIMODAL_MODEL)
    # imageContent = Part.from_image(Image.load_from_file(image_uri))

        # Based on the provided file, answer query from the user in plain english and summarize in a table. 

    imageContent = Part.from_uri(gcs_uri, mime_type="image/jpeg")

    final_prompt = f""" [Context] 
        You are a helpful assistant specialized in financial statement analysis you will have a step by step approach to the query from the user. 
        As an helpful assistant you will always give as much detail as possible of your step by step thinking.
    [Query]
        {prompt}
    [Output]
        Provide your step by step process thinking.
        Always provide the result as a table. 
    """

    contents = [
        imageContent,
        final_prompt
    ]
    responses = model.generate_content(
        contents,  
        generation_config={
            "max_output_tokens": 2048,
            "temperature": 0,
            "top_p": 1,
            "top_k": 1
            },
        stream=True)
    
    responses = list(responses)
    final_response = ""
    try:
        for response in responses:
            final_response = final_response + response.candidates[0].content.parts[0].text
    except IndexError as e:
        print(f"Exception has occured: {e}")
        return final_response

    return final_response

def get_response_from_image2(prompt:str, gcs_uri:str) -> str:
    model = GenerativeModel(MULTIMODAL_MODEL)
    imageContent = Part.from_uri(gcs_uri, mime_type="image/jpeg")

        # Based on the provided file, answer query from the user in plain english and summarize in a table. 


    final_prompt = f""" [Context] 
        You are a helpful assistant specialized in financial statement analysis you will have a step by step approach to the query from the user. 
        As an helpful assistant you will always give as much detail as possible of your step by step thinking.
    [Query]
        {prompt}
    [Output]
        Provide your step by step process thinking.
        Always provide the result as a table. 
    """

    contents = [
        imageContent,
        final_prompt
    ]
    responses = model.generate_content(
        contents,  
        generation_config={
            "max_output_tokens": 2048,
            "temperature": 0,
            "top_p": 1,
            "top_k": 1
            },
        stream=True)
    
    responses = list(responses)
    final_response = ""
    try:
        for response in responses:
            final_response = final_response + response.candidates[0].content.parts[0].text
    except IndexError as e:
        print(f"Exception has occured: {e}")
        return final_response

    return final_response
