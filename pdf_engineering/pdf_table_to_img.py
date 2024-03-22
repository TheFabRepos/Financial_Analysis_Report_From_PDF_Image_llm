import fitz  # import package PyMuPDF
#from vertexai.preview.generative_models import GenerativeModel, Part
#from PIL import Image as PIL_Image
from pdf2image import convert_from_bytes
from  PIL.PpmImagePlugin import PpmImageFile
import io
#from google.cloud import storage



def list_table_in_pdf_from_file(pdf_file_path:str) -> list[int]:
  """Lists all the tables in a PDF file.

  Args:
    pdf_file: The PDF file to list the tables from.

  Returns:
    A list of the tables in the PDF file.
  """

  pdf_file_bytes: bytes = None
  with open(pdf_file_path, "rb") as f:
      pdf_file_bytes = f.read()

  page_list = []

  doc = fitz.open("pdf", pdf_file_bytes)
  for page in doc:
    tabs = page.find_tables()
    if len(tabs.tables) > 0:
      page_list.append(page.number) #index start at 0
                   
  return page_list

def convert_pdf_to_image_from_file(pdf_file_path:str):
    """Converts a PDF file to a list of images.

    Args:
      pdf_file_path: The path to the PDF file to convert.

    Returns:
      A list of images.
    """

    pdf_file_bytes: bytes = None
    with open(pdf_file_path, "rb") as f:
      pdf_file_bytes = f.read()
    images = convert_from_bytes(pdf_file_bytes)
    return images

def convert_ppm_to_file(ppm_image: PpmImageFile, file_path_file_name:str):
  """Converts a PPM image to a Vertex AI Image object.

  Args:
    ppm_image: The PPM image to convert.

  Returns:
    Nil
  """
  ppm_image.save(file_path_file_name)
  