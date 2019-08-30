#!/usr/bin/env bash

apt install -y python >> /tmp/install.log 2>&1
apt install -y python-pip >> /tmp/install.log 2>&1
apt-get update >> /tmp/install.log 2>&1
apt-get install -yq build-essential python-pip rsync >> /tmp/install.log 2>&1

#Set up a GCP Console project from Command Line:
gcloud init >> /tmp/install.log 2>&1

mkdir /opt/snowflake >> /tmp/install.log 2>&1

cd /opt/snowflake >> /tmp/install.log 2>&1
pwd >> /tmp/install.log 2>&1

gcloud source repos clone Billing --project=cardinal-data-piper-sbx >> /tmp/install.log 2>&1
cd Billing >> /tmp/install.log 2>&1
pwd >> /tmp/install.log 2>&1
git checkout snowflake >> /tmp/install.log 2>&1
cp /opt/snowflake/Billing/snowflake/source/snowflake_cron_schedule /etc/cron.d/snowflake_cron_schedule >> /tmp/install.log 2>&1
pip install -r /opt/snowflake/Billing/snowflake/source/requirements.txt >> /tmp/install.log 2>&1
python /opt/snowflake/Billing/snowflake/source/main.py >> /tmp/install.log 2>&1




