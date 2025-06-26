import boto3
import time

dynamodb = boto3.client('dynamodb', endpoint_url="http://localhost:4566")
s3 = boto3.client('s3', endpoint_url="http://localhost:4566")

def test_s3_to_dynamodb_flow():
    bucket_name = "sqsblogstack-inventoryupdatesbucketfe-6ce910e2" 
    test_file = "sqs_blog/sample_file.csv"

    
    # Upload file to trigger Lambda > SQS > Lambda
    s3.upload_file(test_file, bucket_name, test_file)

    time.sleep(5)  # Wait for async processing

    # Check if item landed in DynamoDB
    response = dynamodb.scan(TableName="SqsBlogStack-InventoryUpdates8C5B878A-2b86095d")
    items = response.get("Items", [])
    
    assert len(items) > 0
