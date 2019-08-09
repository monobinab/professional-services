from google.cloud import bigquery
from datetime import datetime, timedelta
import constants
import os
import logging


def get_env_var(key_name):
    """
    Get the environment variables and save it to a variable.
    :param key_name: e.g. key_file
    """
    return os.environ.get(key_name, 'Key name is not set')


def setup():
    key_file = get_env_var(constants.Constants.KEY_FILE)
    bucket_name = get_env_var(constants.Constants.BUCKET_NAME)
    dest_project_id = get_env_var(constants.Constants.DEST_PROJECT_ID)
    dest_dataset_id = get_env_var(constants.Constants.DEST_DATASET_ID)
    dest_table_id = get_env_var(constants.Constants.DEST_TABLE_ID)
    source_table_id = get_env_var(constants.Constants.SOURCE_TABLE_ID)
    source_dataset_id = get_env_var(constants.Constants.SOURCE_DATASET_ID)
    source_project_id = get_env_var(constants.Constants.SOURCE_PROJECT_ID)
    dump_file_name_basename = get_env_var(constants.Constants.DUMP_FILE_NAME)
    yesterday_timestamp = datetime.now() - timedelta(days=1)
    yesterday = yesterday_timestamp.strftime("%Y-%m-%d")
    dump_file_name = dump_file_name_basename + "_" + yesterday + ".json"
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.ERROR)
    return (key_file, bucket_name, dest_project_id, dest_dataset_id, dest_table_id, source_table_id, source_dataset_id,
            source_project_id, dump_file_name)


def extract_billing_delta_table(bucket_name, dump_file_name, project, dataset_id, table_id):

    client = bigquery.Client.from_service_account_json(key_file)
    destination_uri = "gs://{}/{}".format(bucket_name, dump_file_name)
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


def load_interim_delta_table(dest_project_id, dest_dataset_id, dest_table_id):
    client = bigquery.Client.from_service_account_json(key_file)
    job_config = bigquery.QueryJobConfig()
    # Set the destination table
    table_ref = client.dataset(dest_dataset_id).table(dest_table_id)
    job_config.destination = table_ref
    job_config.write_disposition = 'WRITE_TRUNCATE'

    sql = """
        SELECT *
        FROM 
        `data-analytics-pocs.billing.gcp_billing_export_v1_0090FE_ED3D81_AF8E3B`
        where cast(FORMAT_TIMESTAMP("%Y-%m-%d", _PARTITIONTIME) as date) = date_sub(current_date(), interval 1 day)
        ;
    """

    # Start the query, passing in the extra configuration.
    query_job = client.query(
        sql,
        # Location must match that of the dataset(s) referenced in the query
        # and of the destination table.
        location='US',
        job_config=job_config)  # API request - starts the query

    query_job.result()  # Waits for the query to finish
    print('Query results loaded to table {}'.format(table_ref.path))


if __name__ == '__main__':
    (key_file, bucket_name, dest_project_id, dest_dataset_id, dest_table_id, source_table_id, source_dataset_id,
                                                                source_project_id, dump_file_name) = setup()
    load_interim_delta_table(dest_project_id, dest_dataset_id, dest_table_id)
    extract_billing_delta_table(bucket_name, dump_file_name, dest_project_id, dest_dataset_id, dest_table_id)


