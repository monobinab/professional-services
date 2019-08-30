#!/usr/bin/env bash

touch /tmp/test.txt >> /tmp/install.log 2>&1
apt-get update >> /tmp/install.log 2>&1
apt-get install -yq build-essential python-pip rsync >> /tmp/install.log 2>&1

#In order to work from command line and connect to Google Cloud from CLI we have to set Up Google Cloud SDK:

pip install google-cloud-storage >> /tmp/install.log 2>&1

echo "test 1" >> /tmp/install.log 2>&1
#Set up a GCP Console project from Command Line:

gcloud init >> /tmp/install.log 2>&1

#Create Service Account:

gcloud iam service-accounts create snowflake-vm-test >> /tmp/install.log 2>&1
gcloud iam service-accounts keys create ../.gcp/data-piper-folder-test_key.json --iam-account snowflake-vm-test@snowflake-vm-test.iam.gserviceaccount.com >> /tmp/install.log 2>&1

echo "test 2" >> /tmp/install.log 2>&1
#Assign multiple roles to Service Account based on your need:

gcloud projects add-iam-policy-binding snowflake-vm-test --member serviceAccount:snowflake-vm-test@snowflake-vm-test.iam.gserviceaccount.com --role roles/resourcemanager.organizationAdmin >> /tmp/install.log 2>&1

gcloud projects add-iam-policy-binding snowflake-vm-test --member serviceAccount:snowflake-vm-test@snowflake-vm-test.iam.gserviceaccount.com --role roles/browser >> /tmp/install.log 2>&1

gcloud projects add-iam-policy-binding snowflake-vm-test --member serviceAccount:snowflake-vm-test@snowflake-vm-test.iam.gserviceaccount.com --role roles/owner >> /tmp/install.log 2>&1

#Python Packages that need to be installed from command line:

pip install google-cloud-resource-manager >> /tmp/install.log 2>&1
pip install google-api-python-client >> /tmp/install.log 2>&1
pip install oauth2client >> /tmp/install.log 2>&1
pip install --upgrade google-api-python-client >> /tmp/install.log 2>&1
pip install --upgrade google-cloud-bigquery >> /tmp/install.log 2>&1

echo "test 3" >> /tmp/install.log 2>&1
useradd monobina >> /tmp/install.log 2>&1
su - monobina >> /tmp/install.log 2>&1
whoami >> /tmp/install.log 2>&1
mkdir /tmp/snowflake >> /tmp/install.log 2>&1
chmod 777 /tmp/snowflake >> /tmp/install.log 2>&1
cd /tmp/snowflake >> /tmp/install.log 2>&1
git clone git@github.com:monobinab/professional-services.git >> /tmp/install.log 2>&1


