import json
import boto3
import os
import zipfile
import urllib.parse
import logging

logger = logging.getLogger()

logger.info('Loading function')

stepfunction = boto3.client('stepfunctions')

def lambda_handler(event, context):
    s3_key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
    target_key = ""
    target_bucket = os.environ['TargetBucket']
    
    tmp_filename='/tmp/file.zip'

    s3 = boto3.resource('s3')
    s3.Bucket(event["Records"][0]["s3"]["bucket"]["name"]).download_file(s3_key, tmp_filename)
    zfile = zipfile.ZipFile('/tmp/file.zip')
    filelist = zfile.namelist()
    print(filelist)
    
    s3_path = ""
    json_dict = {}
    for filename in filelist:
        if not os.path.basename('/tmp/'+filename):
            os.mkdir('/tmp/'+filename)
        else:
            f = open('/tmp/' + str(filename), 'wb')
            data = zfile.read(filename)
            f.write(data)
            f.close()

            if '.json' in filename:
                print('/tmp/'+filename)
                f = open('/tmp/'+filename, 'r', encoding="utf8", errors='ignore')
                json_dict = json.load(f)
            elif '.mp4' in filename:
                print('/tmp/'+filename)
                s3_client = boto3.client('s3')
                s3_client.upload_file('/tmp/'+filename, event["Records"][0]["s3"]["bucket"]["name"], "videos/" + filename)
                s3_path = "s3://" + event["Records"][0]["s3"]["bucket"]["name"] + "/videos/" + filename
                print(s3_path)
                target_key = "/videos/" + filename
    
    
    if len(json_dict) == 0:
        logger.error("json file does not exist")
        return
    
    if 'lang' in json_dict:
        lang = json_dict['lang']
    else:
        lang = 'en-US'
    
    if s3_path == "":
        logger.error("The object does not exist: s3://" + event["Records"][0]["s3"]["bucket"]["name"] + "/videos/" + filename)
        return
    
    if len(target_key.rsplit('/', 1)) > 1:
        input_str = '{"MediaFileURL": "' + s3_path + '","LanguageCode": "' + lang + '", "FileName": "' + target_key.rsplit('/', 1)[1] + '","OutputBucket": "' + target_bucket + '"}'
    else:
        input_str = '{"MediaFileURL": "' + s3_path + '","LanguageCode": "' + lang + '", "FileName": "' + target_key + '","OutputBucket": "' + target_bucket + '"}'
    print(input_str)
    stepfunction.start_execution(
        stateMachineArn = os.environ['StateMachineArn'],
        input = input_str
    )
