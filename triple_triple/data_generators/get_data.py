import logging
import os
import re
import shutil
import tempfile
import time

import boto3
import pandas as pd


from triple_triple.config import ATHENA_OUTPUT


athena = boto3.client('athena', region_name='us-east-1')
glue = boto3.client('glue', region_name='us-east-1')
s3 = boto3.client('s3', region_name='us-east-1')
# s3 = boto3.resource('s3', region_name='us-east-1')

# initiate logger
logger = logging.getLogger()
logging.getLogger().addHandler(logging.StreamHandler())
logger.setLevel('INFO')


def list_for_sql(some_list: list):
    """
        Used in sql WHERE column IN ().
        Example: Converts [1, 2, 3] to '(1, 2, 3)'
                 Converts [1] to '(1)'
    """
    return re.sub(',\)', ')', str(tuple(some_list)))

    # if len(some_list) == 1:
    #     return '({})'.format(some_list[0])
    # else:
    #     return str(tuple(some_list))


def execute_athena_query(
        query: str,
        database: str,
        output_filename: str,
        boto3_client=athena  # : botocore.client.Athena
):
    """
        This function executes a query and stores it in the
        default athena query folder in s3.
    
    Parameters
    ----------
        query: `str`
            The sql query desired to be executed

        database: `str`
            The database where tables are stored
        
        output_filename: `str`
            A folder within the default aws-athena-query to store the results
            of the query
        
        boto3_client: `boto`?
            The boto3.client('athena') client.
    
    Returns
    -------
    A `dict` of the query execution meta data. 
    This has two keys:
        `QueryExecutionId` and `ResponseMetadata`.
    """
    execute_response = boto3_client.start_query_execution(
        QueryString=query,
        QueryExecutionContext={'Database': database},
        ResultConfiguration={
            'OutputLocation': os.path.join('s3://', ATHENA_OUTPUT, output_filename)
        }
    )
    execution_id = execute_response['QueryExecutionId']
    response = boto3_client.get_query_execution(QueryExecutionId=execution_id)
    response_status = response['QueryExecution']['Status']['State']

    if response_status in ['SUCCEEDED', 'RUNNING']:
        logger.info('Status is {}'.format(response_status))
        return execute_response

    elif response_status == 'FAILED':
        msg = response['QueryExecution']['StateChangeReason']
        logger.error(msg)
        
        return msg

    else:
        logger.error('Something is up. Response is neither SUCCEEDED nor RUNNING nor FAILED.')
        return response_status


def get_query_s3filepath(
        execute_athena_response: dict,
        boto3_client=athena  # : botocore.client.Athena
):
    """
        This function takes the response of the `execute_athena_query` response 
        function and returns the location of the results on s3.

    Parameters
    ----------
        execute_athena_response: `dict`
            This is the dict returned by `execute_athena_query`.
        boto3_client:
            The boto3.client('athena') client.
    Returns
    -------
        A `dict` of the query execution meta data. 
        This has two keys:
            `QueryExecution` and `ResponseMetadata`.
    """

    execution_id = execute_athena_response['QueryExecutionId']
    response = boto3_client.get_query_execution(QueryExecutionId=execution_id)

    return response['QueryExecution']['ResultConfiguration']['OutputLocation']


def s3download(s3_filepath: str, bucket_name: str = ATHENA_OUTPUT):
    # gettempdir() returns the name of the directory used for temporary files
    # logger.info('Creating tmp directory')
    tmp_dir = tempfile.mkdtemp()
    temp_name = os.path.basename(s3_filepath)
    output_filepath = os.path.join(tmp_dir, temp_name)

    try:
        # logger.info('Downloading file from s3')
        s3.download_file(
            Bucket=bucket_name,
            Key=s3_filepath,
            Filename=output_filepath
        )

        return output_filepath

    except boto3.exceptions.botocore.client.ClientError as err:
        logger.error(err)
        raise


def check_key_exists(
        bucket_name: str,
        key: str,
        wait_time: int = 60,
        increment: int = 2 # check every 5 seconds
):
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=key)

    t = 0
    while not response.get('Contents', []) and t < wait_time:
        # wait increment (seconds)
        time.sleep(increment)

        t += increment
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=key)

    if response.get('Contents', []):
        logger.info('It took {} seconds for the file appear'.format(t))
        return 1
    else:
        logger.info('File did not appear in {} seconds'.format(wait_time))
        return 0


def athena_to_pandas(
        query: str,
        output_filename: str,
        database: str = 'nba',
        output_bucket: str = ATHENA_OUTPUT,
        wait_time: int = 60,
        increment: int = 2
):

    response = execute_athena_query(
        query=query,
        database=database,
        output_filename=output_filename
    )
    
    key = '{}/{}.csv'.format(output_filename, response['QueryExecutionId'])
    # wait for file to load
    file_exists = check_key_exists(
        bucket_name=output_bucket,
        key=key,
        wait_time=wait_time,
        increment=increment)

    local_filepath = s3download(
        bucket_name=output_bucket,
        s3_filepath=key
    )

    # read in the data
    df = pd.read_csv(local_filepath)

    # remove filepath
    shutil.rmtree(os.path.split(local_filepath)[0])

    return df


def check_table_exists(
        database_name: str,
        table_name: str,
        max_time: int = 0
):
    response = glue.get_tables(DatabaseName=database_name, Expression=table_name)

    time_to_appear = 0
    time_increment = 1

    while not response['TableList'] and time_to_appear <= max_time:    
        time.sleep(time_increment)
        time_to_appear += time_increment

        response = glue.get_tables(DatabaseName=database_name, Expression=table_name)

    if response['TableList']:
        logger.info('It took {} seconds for the table to appear'.format(time_to_appear))
        return 1
    else:
        logger.info('Table did not appear in the max time of {} seconds'.format(max_time))
        return 0


def get_query_response(
        execution_id: str,
        max_time: int = 5,
        boto3_client=athena
):
    
    response = boto3_client.get_query_execution(QueryExecutionId=execution_id)
    status = response['QueryExecution']['Status']['State']

    time_to_appear = 0
    time_increment = 1

    while (status == 'RUNNING' and time_to_appear <= max_time):
        time.sleep(time_increment)
        time_to_appear += time_increment

        response = boto3_client.get_query_execution(QueryExecutionId=execution_id)
        status = response['QueryExecution']['Status']['State']

    if time_to_appear > max_time + 1:
        print(status)
        print(time_to_appear)
        logger.info('Execution did not finish in the max time of {} seconds'.format(max_time))
        return []
    else:
        print(status)
        print(time_to_appear)
        # return query results
        return boto3_client.get_query_results(QueryExecutionId=execution_id)


def get_query_results(
        query: str,
        output_filename: str,
        max_time: int, # maximum time to just if query executed
        database: str = 'nba'
):

    execute_response = execute_athena_query(
        query=query,
        database=database,
        output_filename=output_filename,
    )
    execution_id = execute_response['QueryExecutionId']

    # query results
    return get_query_response(
        execution_id=execution_id,
        max_time=max_time
    )


def check_view_exists(
        database: str,
        view_name: str,
        max_time: int = 0,
        boto3_client = athena
):

    query_results = get_query_results(
        query="SHOW VIEWS IN {} LIKE '{}'".format(database, view_name),
        output_filename='show_{}'.format(view_name),
        max_time=max_time,
        database=database
    )

    if query_results['ResultSet']['Rows']:
        return 1
    else:
        return 0


def get_bucket_content(bucket_name: str, prefix: str, delimiter: str = '/'):
    """
    This function returns the elements ('subfolders) in the given `bucket_name`
    with keys beginning with the given `prefix`.

    Parameters
    ----------
    bucket_name: `str`
        The s3 bucket name containing the data
    
    prefix: `str`
        The full key prefix, ending in '/'.
        Example: 'gameposition/season=2015-2016/'
    
    delimiter: `str`
        For 'subfolders', use '/'.
        For all 'files', use ''.

    Returns
    ------
    A list of dictionaries. Each dictionary has key 'Prefix'
    and value equal to the `prefix` + subfolder.
    Example: 'gameposition/season=2015-2016/gameid=0021500663/'

    """
    response = s3.list_objects(
        Bucket=bucket_name,
        Prefix=prefix,
        Delimiter=delimiter
    )

    if delimiter == '/':
        # returns 'subfolders'
        return response.get('CommonPrefixes')
    elif delimiter == '':
        # returns all 'files'
        return [file['Key'] for file in response['Contents']]


def copy_bucket_contents(
        copy_source_keys: list,  # list of all files to move
        destination_bucket: str,
        destination_folder: str,
        s3client
):
    for file in copy_source_keys:
        copy_params = {'Bucket': destination_bucket, 'Key': file}
        # removes source_folder
        destination_suffix = '/'.join(file.split('/')[1:])
        destination_key = '{}/{}'.format(destination_folder,
                                         destination_suffix)

        logger.info('Copying {} in to {}'.format(file, destination_folder))
        # copy object in to destination
        s3client.copy_object(
            Bucket=destination_bucket,
            CopySource=copy_params,
            Key=destination_key
        )


def remove_bucket_contents(
        bucket: str,
        key: str,
        s3client
):

    logger.info('Removing {}'.format(key))
    # delete object from source
    s3client.delete_object(
        Bucket=bucket,
        Key=key
    )
