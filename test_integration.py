import os
import boto3
import time

os.environ['AWS_ACCESS_KEY_ID'] = 'test'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'test'
os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'

dynamodb = boto3.client('dynamodb', endpoint_url="http://localhost:4566")
s3 = boto3.client('s3', endpoint_url="http://localhost:4566")

def test_s3_to_dynamodb_flow():
   
    target_bucket_prefix = "sqsblogstack-inventoryupdatesbucketfe-"
    response = s3.list_buckets()
    bucket_name = next((bucket['Name'] for bucket in response['Buckets'] if bucket['Name'].startswith(target_bucket_prefix)), None)
    assert bucket_name is not None, "Bucket not found"
   

    target_ddb_prefix = "SqsBlogStack-InventoryUpdates"
    response = dynamodb.list_tables()
    table_name = next((table for table in response['TableNames'] if table.startswith(target_ddb_prefix)), None)

    test_file = "sqs_blog/sample_file.csv"
    s3.upload_file(test_file, bucket_name, test_file)

    time.sleep(5)

    response = dynamodb.scan(TableName=table_name)
    items = response.get("Items", [])
    assert len(items) > 0, "No items found in DynamoDB"

