CREATE TABLE IF NOT EXISTS {} WITH (
    external_location = '{}',
    format = 'PARQUET',
    partitioned_by = {},
    parquet_compression = 'SNAPPY'
) AS (
{}
)