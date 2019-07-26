import os

# [directories]

MODULE_HOME = os.path.dirname(__file__)

DATASETS_DIR = os.path.join(MODULE_HOME, 'data')
IMG_DIR = os.path.join(MODULE_HOME, 'img')
SQL_DIR = os.path.join(MODULE_HOME, 'sql')
MOCK_DATASETS_DIR = os.path.join(MODULE_HOME, 'tests', 'fixtures')

# [aws]
AWS_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_PASSWORD = os.environ.get('AWS_SECRET_ACCESS_KEY')
# ATHENA_OUTPUT = os.environ.get('AWS_ATHENA_OUTPUT_DIR')
ATHENA_OUTPUT = 'aws-athena-query-results-401845286067-us-east-1'
