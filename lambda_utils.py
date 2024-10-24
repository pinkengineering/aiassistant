import json
import os
from typing import List
from botocore.exceptions import ClientError
import utils as lambda_helpers

LAMBDA_ROLE = os.environ["LAMBDA_ROLE"]
S3_BUCKET = os.environ["S3_BUCKET"]

def create_lambda_function(
    lambda_client,
    s3,
    code: str,
    function_name: str,
    description: str,
    has_external_python_libraries: bool,
    external_python_libraries: List[str],
) -> str:
    """
    Creates and deploys a Lambda Function, based on what the customer requested.
    Returns the name of the created Lambda function
    """
    print("Creating Lambda function")
    runtime = "python3.12"
    handler = "lambda_function.handler"

    # Create a zip file for the code
    if has_external_python_libraries:
        zipfile = lambda_helpers.create_deployment_package_with_dependencies(
            code, function_name, f"{function_name}.zip", external_python_libraries
        )
    else:
        zipfile = lambda_helpers.create_deployment_package_no_dependencies(
            code, function_name, f"{function_name}.zip"
        )

    try:
        # Upload zip file
        zip_key = f"lambda_resources/{function_name}.zip"
        s3.upload_file(zipfile, S3_BUCKET, zip_key)
        print(f"Uploaded zip to {S3_BUCKET}/{zip_key}")

        response = lambda_client.create_function(
            Code={
                "S3Bucket": S3_BUCKET,
                "S3Key": zip_key,
            },
            Description=description,
            FunctionName=function_name,
            Handler=handler,
            Timeout=30,
            Publish=True,
            Role=LAMBDA_ROLE,
            Runtime=runtime,
        )
        print("Lambda function created successfully")
        print(response)
        deployed_function = response["FunctionName"]
        user_response = f"The function {deployed_function} has been deployed to the customer's AWS account."
        return user_response
    except ClientError as e:
        print(e)
        return f"Error: {e}\n Let me try again..."

def call_lambda_function(lambda_client, function_name, payload={}):
    """
    Invokes a Lambda function with the given payload.
    """
    try:
        response = lambda_client.invoke(
            FunctionName=function_name,
            InvocationType='RequestResponse',  # Synchronous call
            Payload=json.dumps(payload)  # Sending an empty payload if not needed
        )
        # Parse the response
        response_payload = json.loads(response['Payload'].read())
        print(f"Lambda response: {response_payload}")
        return response_payload
    except Exception as e:
        print(f"Error invoking Lambda function: {e}")
        return {"error": str(e)}