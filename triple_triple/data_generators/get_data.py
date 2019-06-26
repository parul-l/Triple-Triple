import logging
import tempfile
import time
import os

import boto3

from triple_triple.config import ATHENA_OUTPUT


athena = boto3.client('athena', region_name='us-east-1')
glue = boto3.client('glue', region_name='us-east-1')
s3 = boto3.client('s3', region_name='us-east-1')
# s3 = boto3.resource('s3', region_name='us-east-1')

# initiate logger
logger = logging.getLogger()
logger.setLevel('INFO')


def list_for_sql(some_list: list):
    """
        Used in sql WHERE column IN ().
        Example: Converts [1, 2, 3] to '(1, 2, 3)'
                 Converts [1] to '(1)'
    """

    if len(some_list) == 1:
        return '({})'.format(some_list[0])
    else:
        return str(tuple(some_list))


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
    return boto3_client.start_query_execution(
        QueryString=query,
        QueryExecutionContext={'Database': database},
        ResultConfiguration={
            'OutputLocation': os.path.join('s3://', ATHENA_OUTPUT, output_filename)
        }
    )


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

