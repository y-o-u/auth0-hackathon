import json
import boto3
import os

stepfunction = boto3.client('stepfunctions')

def lambda_handler(event, context):
    
    s3_path = "s3://" + event["Records"][0]["s3"]["bucket"]["name"] + "/" + event["Records"][0]["s3"]["object"]["key"]
    target_key = event["Records"][0]["s3"]["object"]["key"]
    target_bucket = os.environ['TargetBucket']
    
    if len(target_key.rsplit('/', 1)) > 1:
        input_str = '{"MediaFileURL": "' + s3_path + '","LanguageCode": "en-US", "FileName": "' + target_key.rsplit('/', 1)[1] + '","OutputBucket": "' + target_bucket + '"}'
    else:
        input_str = '{"MediaFileURL": "' + s3_path + '","LanguageCode": "en-US", "FileName": "' + target_key + '","OutputBucket": "' + target_bucket + '"}'
    
    stepfunction.start_execution(
        stateMachineArn = os.environ['StateMachineArn'],
        input = input_str
    )
