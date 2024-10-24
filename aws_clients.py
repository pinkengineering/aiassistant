import boto3
import os

REGION = "us-east-1"

def initialize_clients():
    """Initialize and return the AWS Bedrock, Lambda, and S3 clients."""
    session = boto3.Session()
    bedrock = session.client(service_name="bedrock-runtime", region_name=REGION)
    lambda_client = session.client("lambda", region_name=REGION)
    s3 = session.client("s3", region_name=REGION)
    return bedrock, lambda_client, s3