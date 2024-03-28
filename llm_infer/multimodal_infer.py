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


def extract_table_to_json_from_image(image_uri: str) -> str:
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
