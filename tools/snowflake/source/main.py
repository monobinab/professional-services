
from google.cloud import bigquery
from datetime import datetime, timedelta
import os
import json
import sys
import google.cloud.logging


def extract_billing_delta_table(config_file, logger_name):
    """
       This function has config.json file as input. It will read the config file and get the details and process it.
       :param config_file: config.json  file
       :return: Success or Invalid request
     """

    logging_client = google.cloud.logging.Client()
    logger = logging_client.logger(logger_name)

    logger.log_text('Starting Extracting!')

    # Read the export table, destination temp table, dump file from json config file
    with open(config_file) as json_file:
        config_data = json.load(json_file)


        key_file = config_data['key_file']
        bucket_name = config_data['bucket_name']
        project = config_data['project']
        dest_dataset_id = config_data['dest_dataset_id']
        status_file_name = config_data['status_file_name']

        for export_record in config_data['export_detail']:
            dump_file_name = export_record["dump_file"]
            dest_table_id = export_record["destination_table"]
            export_table = export_record["export_table"]

    client = bigquery.Client.from_service_account_json(key_file)
    yesterday = datetime.strftime(datetime.now() - timedelta(1), '%Y%m%d')
    destination_uri = "gs://{}/{}/{}".format(bucket_name, yesterday, dump_file_name)

    dataset_id, table_id = load_interim_delta_table(key_file, export_table, dest_dataset_id, dest_table_id)
    dataset_ref = client.dataset(dataset_id, project=project)
    table_ref = dataset_ref.table(table_id)

    job_config = bigquery.job.ExtractJobConfig()
    job_config.destination_format = bigquery.DestinationFormat.NEWLINE_DELIMITED_JSON

    extract_job = client.extract_table(
        table_ref,
        destination_uri,
        # Location must match that of the source table.
        location="US",
        job_config=job_config
    )  # API request
    extract_job.result()  # Waits for job to complete.
    print(
        "Exported {}:{}.{} to {}".format(project, dataset_id, table_id, destination_uri)
    )
    create_status_file(bucket_name, yesterday, status_file_name)


def load_interim_delta_table(key_file, export_table, dest_dataset_id, dest_table_id):
    """
    This function creates an interim table by running a SQL on the source table.
    :param key_file: Service Account key file
    :param export_table: GCP exporting source file name
    :param dest_dataset_id: Dataset id where interim table will be stored.
    :param dest_table_id: Interim table id.
    :return: Interim table information
    """
    client = bigquery.Client.from_service_account_json(key_file)
    job_config = bigquery.QueryJobConfig()
    # Set the destination table
    table_ref = client.dataset(dest_dataset_id).table(dest_table_id)
    job_config.destination = table_ref
    job_config.write_disposition = 'WRITE_TRUNCATE'

    sql = "SELECT * FROM `" + export_table + "`" + """ where cast(FORMAT_TIMESTAMP("%Y-%m-%d", export_time) as date) = date_sub(current_date(), interval 1 day); """
    print(sql)

    # Start the query, passing in the extra configuration.
    query_job = client.query(
        sql,
        # Location must match that of the dataset(s) referenced in the query
        # and of the destination table.
        location='US',
        job_config=job_config)  # API request - starts the query

    query_job.result()  # Waits for the query to finish
    print('Query results loaded to table {}'.format(table_ref.path))
    return dest_dataset_id, dest_table_id


def create_status_file(bucket_name, process_status_dir, status_file_name):
    """
    This function creates an empty status file.
    :param bucket_name: GCS Bucket where the file will be created
    :param process_status_dir: Folder in the bucket where file will be created
    :param status_file_name: Status file name
    :return:
    """
    open(status_file_name, 'w+')
    gcs_file_path = "gs://{}/{}".format(bucket_name, process_status_dir)
    cmd = "gsutil cp " + status_file_name + " " + gcs_file_path
    os.system(cmd)
    os.system("rm -f " + status_file_name)


if __name__ == '__main__':

    try:
        config_file = sys.argv[1]
        logger_name = sys.argv[2]
    except IOError:
        print("Please provide config file as argument of the script")
        exit(1)

    extract_billing_delta_table(config_file, logger_name)




