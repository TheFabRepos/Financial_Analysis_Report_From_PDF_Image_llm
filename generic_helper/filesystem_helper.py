import os
from datetime import datetime


def create_tmp_directory(filename_only) -> str:
  
  """Creates a temporary which will be used to do local work (e.g., converting PDF to images, getting JSON data, etc.).

  Args:
    filename_only: The name of the PDF file without the extension.

  Returns:
    The path to the temporary directory.
  """

  temp_directory = "{}/tmp_{}_{}".format(os.getcwd(),filename_only,datetime.now().strftime("%Y%m%d%H%M"))
  os.makedirs(temp_directory, exist_ok=True)
  os.makedirs(os.path.join(temp_directory, "images"), exist_ok=True)
  return temp_directory


def extract_filename (full_name: str) -> str:
    """Extracts the filename from a full path.

    Args:
        full_name: The full path to the file with extension and folder name.


    Returns:
        The filename (with extension) as string
    """

    filename_with_extension = (full_name.split("/")[-1])
    return filename_with_extension