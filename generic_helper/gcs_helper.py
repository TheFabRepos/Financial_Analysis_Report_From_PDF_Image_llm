from google.cloud import storage
from generic_helper import config_helper
from datetime import timedelta
from google import auth
from google.cloud.storage import Client
import datetime



STORAGE_CLIENT = storage.Client()
BUCKET_CLIENT = STORAGE_CLIENT.get_bucket (config_helper.get_config_value("GENERAL", "cloud_storage"))
STORAGE_CLIENT_FOR_SIGNED_URL = storage.Client.from_service_account_json(config_helper.get_config_value("GENERAL", "secret_json_file_path"))
BUCKET_CLIENT_FOR_SIGNED_URL = STORAGE_CLIENT_FOR_SIGNED_URL.get_bucket (config_helper.get_config_value("GENERAL", "cloud_storage"))

def list_pdf_files_in_GCS(bucket_name, folder_name) -> list[storage.Blob]:
  """Lists all the PDF files in a specific folder of a Google Cloud Storage bucket.

  Args:
    bucket_name: The name of the Google Cloud Storage bucket.
    folder_name: The name of the folder to list the files from.

  Returns:
    A list of all the PDF files in the specified folder.
  """

  # Create a client.
  storage_client = storage.Client()

  # Get a list of all the objects in the bucket.
  objects = storage_client.list_blobs(bucket_name)

  # Filter the list of objects to only include PDF files.
  pdf_files = [object for object in objects if object.content_type == "application/pdf"]

  # Filter the list of objects to only include objects in the specified folder.
  folder_objects = [object for object in pdf_files if object.name.startswith(folder_name)]

  return folder_objects

def get_file_from_GCS(bucket_name, folder_name) -> list[storage.Blob]:
  """Lists all the PDF files in a specific folder of a Google Cloud Storage bucket.

  Args:
    bucket_name: The name of the Google Cloud Storage bucket.
    folder_name: The name of the folder to list the files from.

  Returns:
    A list of all the PDF files in the specified folder.
  """

  # Create a client.
  storage_client = storage.Client()

  # Get a list of all the objects in the bucket.
  objects = storage_client.list_blobs(bucket_name)

  # Filter the list of objects to only include PDF files.
  pdf_files = [object for object in objects if object.content_type == "application/pdf"]

  # Filter the list of objects to only include objects in the specified folder.
  folder_objects = [object for object in pdf_files if object.name.startswith(folder_name)]

  return folder_objects

# def upload_file_to_GCS(bucket_name, folder_name):
#   storage_client = storage.Client()
#   storage_client.

# bucket = client.get_bucket('mybucket')
# blob = bucket.blob('myfile')
# blob.upload_from_filename('myfile')
  
def upload_file_to_GCS (directory, full_file_path):
    file_name = full_file_path.split('/')[-1]
    blob = BUCKET_CLIENT.blob(f"{directory}/{file_name}")
    blob.upload_from_filename(f"{full_file_path}")

def get_url_from_file_GCS (directory, file_name):

    blob = BUCKET_CLIENT_FOR_SIGNED_URL.blob(f"{directory}/{file_name}") # name of file to be saved/uploaded to storage
    signed_URL = blob.generate_signed_url(
        version='v4',
        expiration=datetime.timedelta(minutes=1),
        method='GET') 

    return signed_URL



