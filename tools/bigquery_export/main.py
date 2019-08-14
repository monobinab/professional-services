from google.cloud import bigquery
from datetime import datetime, timedelta
import os
import google.cloud.logging as cloud_logging



class Constants:
    KEY_FILE = 'key_file'
    BUCKET_NAME = 'bucket_name'
    DEST_PROJECT_ID = "dest_project_id"
    DEST_DATASET_ID = "dest_dataset_id"
    DEST_TABLE_ID = "dest_table_id"
    SOURCE_TABLE_ID = "source_table_id"
    SOURCE_DATASET_ID = "source_dataset_id"
    SOURCE_PROJECT_ID = "source_project_id"
    DUMP_FILE_NAME = "dump_file_name"


def get_env_var(key_name):
    """
    Get the environment variables and save it to a variable.
    :param key_name: e.g. key_file
    """
    return os.environ.get(key_name, 'Key name is not set')


def setup():
    key_file = get_env_var(Constants.KEY_FILE)
    bucket_name = get_env_var(Constants.BUCKET_NAME)
    dest_project_id = get_env_var(Constants.DEST_PROJECT_ID)
    dest_dataset_id = get_env_var(Constants.DEST_DATASET_ID)
    dest_table_id = get_env_var(Constants.DEST_TABLE_ID)
    source_table_id = get_env_var(Constants.SOURCE_TABLE_ID)
    source_dataset_id = get_env_var(Constants.SOURCE_DATASET_ID)
    source_project_id = get_env_var(Constants.SOURCE_PROJECT_ID)
    dump_file_name_basename = get_env_var(Constants.DUMP_FILE_NAME)
    yesterday_timestamp = datetime.now() - timedelta(days=1)
    yesterday = yesterday_timestamp.strftime("%Y-%m-%d")
    dump_file_name = dump_file_name_basename + "_" + yesterday + ".json"
    #logging.basicConfig(format='%(asctime)s %(message)s', level=logging.ERROR)
    return (key_file, bucket_name, dest_project_id, dest_dataset_id, dest_table_id, source_table_id, source_dataset_id,
            source_project_id, dump_file_name)


def http_extract_billing_delta_table(request):
    request_args = request.args
    logging_client = cloud_logging.Client()
    log_name = 'cloudfunctions.googleapis.com%2Fcloud-functions'
    logger = logging_client.logger(log_name)
    logger.log_text('Reading parameters')

    if request_args and 'bucket_name' in request_args and 'dump_file_name' in request_args \
            and 'project' in request_args and 'dest_dataset_id' in request_args and 'dest_table_id' in request_args:
        key_file = request_args['key_file']
        bucket_name = request_args['bucket_name']
        dump_file_name = request_args['dump_file_name']
        project = request_args['project']
        dest_dataset_id = request_args['dest_dataset_id']
        dest_table_id = request_args['dest_table_id']

        # logger.info('Will execute extract function')
        # console.info("running extract")
        extract_billing_delta_table(key_file, bucket_name, dump_file_name, project, dest_dataset_id, dest_table_id)

        return "Success!"
    else:
        return "Invalid request"


def extract_billing_delta_table(key_file, bucket_name, dump_file_name, project, dest_dataset_id, dest_table_id):

    client = bigquery.Client.from_service_account_json(key_file)
    #client = bigquery.Client()
    destination_uri = "gs://{}/{}".format(bucket_name, dump_file_name)
    dataset_id, table_id = load_interim_delta_table(key_file, dest_dataset_id, dest_table_id)
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


def load_interim_delta_table(key_file, dest_dataset_id, dest_table_id):
    client = bigquery.Client.from_service_account_json(key_file)
    #client = bigquery.Client()
    job_config = bigquery.QueryJobConfig()
    # Set the destination table
    table_ref = client.dataset(dest_dataset_id).table(dest_table_id)
    job_config.destination = table_ref
    job_config.write_disposition = 'WRITE_TRUNCATE'

    sql = """
                SELECT *
                FROM 
                `data-analytics-pocs.billing.gcp_billing_export_v1_0090FE_ED3D81_AF8E3B`
                --`cardinal-data-piper-sbx.public.gcp_billing_export_v1_EXAMPL_E0XD3A_DB33F1`
                where cast(FORMAT_TIMESTAMP("%Y-%m-%d", _PARTITIONTIME) as date) = date_sub(current_date(), interval 1 day)
                limit 1000;
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
    return dest_dataset_id, dest_table_id


if __name__ == '__main__':

    # (key_file, bucket_name, dest_project_id, dest_dataset_id, dest_table_id, source_table_id, source_dataset_id,
    #                                                             source_project_id, dump_file_name) = setup()
    # extract_billing_delta_table(bucket_name, dump_file_name, dest_project_id, dest_dataset_id, dest_table_id)
    request_args = dict()
    request_args['key_file'] = "cardinal-data-piper-sbx.json"
    request_args['bucket_name'] = "snowflake_project"
    request_args['dump_file_name'] = "billing_export_delta"
    request_args['project'] = "cardinal-data-piper-sbx"
    request_args['dest_dataset_id'] = "monobina_sbx"
    request_args['dest_table_id'] = "billing_export_delta"


    http_extract_billing_delta_table(request_args)


