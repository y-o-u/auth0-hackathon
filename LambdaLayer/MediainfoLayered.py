#######################################################################
#
# This code shows how to use mediainfo from AWS Lambda. 
#
# PREREQUISITES:
#   Set region in AWS_REGION environment variable in the Lamdba environment
#
# USAGE:
#   See https://www.bigendiandata.com/2019-12-10-MediaInfo_AWS_Lambda/.
# 
# USEFUL REFERENCES:
#   https://github.com/iandow/mediainfo_aws_lambda
#   https://aws.amazon.com/blogs/compute/extracting-video-metadata-using-lambda-and-mediainfo/
#
#######################################################################


import json
import logging
import boto3
import botocore
import os
from pymediainfo import MediaInfo
from botocore.config import Config
import urllib.parse
from datetime import datetime
import uuid

region = os.environ['AWS_REGION']

def get_signed_url(expires_in, bucket, obj):
    """
    Generate a signed URL
    :param expires_in:  URL Expiration time in seconds
    :param bucket:
    :param obj:         S3 Key name
    :return:            Signed URL
    """
    s3_cli = boto3.client("s3", region_name=region, config = Config(signature_version = 's3v4', s3={'addressing_style': 'virtual'}))
    presigned_url = s3_cli.generate_presigned_url('get_object', Params={'Bucket': bucket, 'Key': obj}, ExpiresIn=expires_in)
    return presigned_url

def put_mediainfo(media_info, title, tags):
    for track in media_info.tracks:
        if track.track_type == 'General':
            file = urllib.parse.unquote_plus(track.file_name)
            folder_name = track.folder_name
            complete_name = track.complete_name
            internet_media_type = track.internet_media_type
            duration = track.duration
            now_time = datetime.now().strftime('%s')
            break
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Contents-Dev')
    
    parsed = urllib.parse.urlparse(complete_name)
    
    title_name = file if title == "" else title
    tags_array = tags.split(',')
    tags_obj = {"tags":tags_array}
    
    response = table.put_item(
       Item={
            'contents_id': str(uuid.uuid4()),
            'title': title_name,
            'file': file,
            'sk': str(now_time),
            'new_arrivals': 0,
            'complete_name': parsed.scheme + "://" + parsed.netloc + parsed.path,
            'folder_name': folder_name,
            'internet_media_type': internet_media_type,
            'duration': duration,
            'createdAt': int(now_time),
            'updatedAt': int(now_time),
            'tags': json.dumps(tags_obj,ensure_ascii=False)
        }
    )
    return response
    
def lambda_handler(event, context):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.info('event parameter: {}'.format(event))
#    tmp_filename='/tmp/my_video.mp4'

#    s3 = boto3.resource('s3')
#    BUCKET_NAME = os.environ.get("BUCKET_NAME")
#    S3_KEY = os.environ.get("S3_KEY")

    BUCKET_NAME = event['MediaFileURL'].split('/')[2]
    #BUCKET_NAME = event['Records'][0]['s3']['bucket']['name']
    S3_KEY = event['MediaFileURL'].split('/', 3)[3]
    #S3_KEY = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
    
    ##########################################################################
    # I'm going to show two ways to invoke MediaInfo:
    #
    # FIRST WAY: download the vidoe file to local storage and provide the local file path as input to MediaInfo. 
    # Disadvantage here is that Lambda only provides 512MB of disk space to save that file.
    #
    # SECOND WAY: Provide an S3 URL as the input to MediaInfo. 
    # Disadvantage here is you must have compiled libcurl support into the MediaInfo library, which I did in https://github.com/iandow/mediainfo_aws_lambda/blob/master/Dockerfile
    ##########################################################################
    
    ##########################################################################
    # FIRST WAY: download the vidoe file to local storage and provide the local file path as input to MediaInfo.
    ##########################################################################

#    try:
#        s3.Bucket(BUCKET_NAME).download_file(S3_KEY, tmp_filename)
#    except botocore.exceptions.ClientError as e:
#        if e.response['Error']['Code'] == "404":
#            print("The object does not exist: s3://" + BUCKET_NAME + S3_KEY)
#        else:
#            raise
#
#    media_info = MediaInfo.parse(tmp_filename, library_file='/opt/libmediainfo.so.0')
#
#    print(str(media_info.to_json()))
#
#    for track in media_info.tracks:
#        if track.track_type == 'Video':
#            print("track info: " + str(track.bit_rate) + " " + str(track.bit_rate_mode)  + " " + str(track.codec))

    ##########################################################################
    # SECOND WAY: Provide an S3 URL as the input to MediaInfo.
    ##########################################################################

    SIGNED_URL_EXPIRATION = 300     # The number of seconds that the Signed URL is valid

    try:
        # Generate a signed URL for the uploaded asset
        signed_url = get_signed_url(SIGNED_URL_EXPIRATION, BUCKET_NAME, S3_KEY)
        # Launch MediaInfo
        media_info = MediaInfo.parse(signed_url, library_file='/opt/libmediainfo.so.0')
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist: s3://" + BUCKET_NAME + S3_KEY)
        raise
    
    print(media_info.to_json())
    
    res = put_mediainfo(media_info, event['Title'],event['Tags'])
    print(res)
    
    # Finish the Lambda function with an HTTP 200 status code:
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": str(media_info.to_json())
        }),
    }

