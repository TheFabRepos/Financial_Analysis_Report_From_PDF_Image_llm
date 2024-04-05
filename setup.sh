sudo apt-get install poppler-utils
gcloud config set project <projectID>
gcloud auth application-default login
gcloud auth application-default set-quota-project <projectID>

## Create a service account with Storage Admin permission on the storage bucket (te create SAS signature aginst the storage)