sudo apt-get install poppler-utils
gcloud config set project testfab-362608
gcloud auth application-default login
gcloud auth application-default set-quota-project testfab-362608

## Create a service account with Storage Admin permission on the storage bucket