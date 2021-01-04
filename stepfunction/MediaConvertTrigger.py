import json
import urllib.parse
import boto3
import os
from boto3.dynamodb.conditions import Key
import uuid

s3 = boto3.client('s3')
mediaconvert =  boto3.client('mediaconvert', region_name='ap-northeast-1', endpoint_url='https://1muozxeta.mediaconvert.ap-northeast-1.amazonaws.com')
dynamodb = boto3.resource('dynamodb')
folder = str(uuid.uuid4())
outputDomain = "assets.auth.classmethod.net"

def lambda_handler(event, context):
    inputFile = event['MediaFileURL']
    file_name_noextention = event['FileName'].rsplit('.', 1)[0]
    outputKeyHls = "s3://auth0-hack-output-533554244959/hls/" + folder + "/" + file_name_noextention
    outputKeyThumbnail = "s3://auth0-hack-output-533554244959/thumbnail/" + folder + "/" + file_name_noextention
    
    try:
        # Load job.json from disk and store as Python object: job_object
        with open("job.json", "r") as jsonfile:
            job_object = json.load(jsonfile)
            
        # Input/Output Setting
        job_object["OutputGroups"][0]["OutputGroupSettings"]["HlsGroupSettings"]["Destination"] = outputKeyHls
        job_object["OutputGroups"][1]["OutputGroupSettings"]["FileGroupSettings"]["Destination"] = outputKeyThumbnail
        job_object["Inputs"][0]["FileInput"] = inputFile

        # Exec MediaConvert's job
        response = mediaconvert.create_job(
          JobTemplate='arn:aws:mediaconvert:ap-northeast-1:533554244959:jobTemplates/Auth0Hack-JobTemplate',
          Queue='arn:aws:mediaconvert:ap-northeast-1:533554244959:queues/Default',
          Role='arn:aws:iam::533554244959:role/MediaConvert-SVC-Role',
          Settings=job_object
        )
        
        dynamodb_table = dynamodb.Table('Contents-Dev')
        response = dynamodb_table.query(
            IndexName='file-sk-index',
            KeyConditionExpression=Key('file').eq(event['FileName'].rsplit('.', 1)[0])
        )
        dynamodb_table.update_item(
            Key = {
                'contents_id': response['Items'][0]['contents_id'],
                'sk': response['Items'][0]['sk']
            },
            UpdateExpression = "set hls_url=:hu, thumbnail_url=:tu",
            ExpressionAttributeValues = {
                ':hu': "https://" + outputDomain + "/hls/" + folder + "/" + file_name_noextention + ".m3u8",
                ':tu': "https://" + outputDomain + "/thumbnail/" + folder + "/" + file_name_noextention + ".0000003.jpg"
            }
        )
    except Exception as e:
        print(e)
        print('Error.')
        raise e