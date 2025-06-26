import boto3
import time

dynamodb = boto3.client('dynamodb', endpoint_url="http://localhost:4566")
s3 = boto3.client('s3', endpoint_url="http://localhost:4566")

def test_s3_to_dynamodb_flow():
    # As of now, the bucket_name and table_name are hardcoded.
    # In a real-world scenario, these should be parameterized or configured.
    # Ensure that we use Python's prefix functionality to avoid hardcoding.

    target_bucket_prefix = "sqsblogstack-inventoryupdatesbucketfe-"
    response = s3.list_buckets()
    bucket_name = next((bucket['Name'] for bucket in response['Buckets'] if bucket['Name'].startswith(target_bucket_prefix)), None)
    assert bucket_name is not None, "Bucket not found"
    test_file = "sqs_blog/sample_file.csv"

    
    # Upload file to trigger Lambda > SQS > Lambda
    s3.upload_file(test_file, bucket_name, test_file)

    time.sleep(5)  # Wait for async processing

    # Check if item landed in DynamoDB
    target_ddb_prefix = "SqsBlogStack-InventoryUpdates"
    response = dynamodb.list_tables()
    table_name = next((table for table in response['TableNames'] if table.startswith(target_ddb_prefix)), None)
    assert table_name is not None, "DynamoDB table not found"
    response = dynamodb.scan(TableName=table_name)
    items = response.get("Items", [])
    
    assert len(items) > 0
