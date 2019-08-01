import pyathena
from triple_triple.config import (
    AWS_ID,
    AWS_PASSWORD
)


# pyathena is a lot slower than boto3
# it is faster to execute, get path, download and then upload in to python using boto
# than using pyathena

def get_connection(
    aws_access_key_id: str = AWS_ID,
    aws_secret_access_key: str = AWS_PASSWORD,
    s3_staging_dir: str = 's3://nba-game-info/',
    region_name: str = 'us-east-1'
):
    return pyathena.connect(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        s3_staging_dir=s3_staging_dir,
        region_name=region_name
    )