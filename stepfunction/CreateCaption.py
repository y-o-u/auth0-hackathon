import json
import boto3
import ast
import os
import math
from boto3.dynamodb.conditions import Key
import uuid

s3 = boto3.resource('s3')
dynamodb = boto3.resource('dynamodb')
translate = boto3.client('translate')
folder = str(uuid.uuid4())
outputDomain = "assets.auth.classmethod.net"

def create_timecode(time):
    hour = math.floor(float(time) / 3600)
    time_str = str(hour).zfill(2)
    minite = math.floor(float(time) / 60)
    time_str = time_str + ":" + str(minite).zfill(2)
    second = float(time) % 60
    time_str = time_str + ":" + str("{:.3f}".format(second)).zfill(6)
    return time_str

def translate_text(text, source, target):
    result = translate.translate_text(
        Text = text,
        SourceLanguageCode = source,
        TargetLanguageCode = target
    )
    return result.get('TranslatedText')

def lambda_handler(event, context):
    s3bucket = event['transcribeJobStatus']['outputS3bucket']
    s3key = event['transcribeJobStatus']['outputS3key']
    
    obj = s3.Object(s3bucket, s3key)
    body = obj.get()['Body'].read().decode('utf-8')
    #dict_sample = ast.literal_eval(body)
    items = json.loads(body)['results']['items']
    
    fp_ja = open('/tmp/tmp_ja.vtt', 'w')
    fp_en = open('/tmp/tmp_en.vtt', 'w')
    
    fp_ja.write("WEBVTT\n")
    fp_ja.write("\n")
    fp_en.write("WEBVTT\n")
    fp_en.write("\n")
    
    tmp_start_time = items[0]['start_time']
    tmp_end_time = 0
    tmp_str = ""
    init_flag = True
    for item in items:
        if 'start_time' in item and 'end_time' in item:
            
            if init_flag == True:
                tmp_end_time = item['end_time']
                if event['createTranscribeJob']['sourceLanguage'] == "en":
                    tmp_str = tmp_str + " " + item['alternatives'][0]['content']
                else:
                    tmp_str = tmp_str + item['alternatives'][0]['content']
                init_flag = False
                continue
            
            if float(item['start_time']) - float(tmp_end_time) > 0.3:
                fp_ja.write(create_timecode(tmp_start_time) + " --> " + create_timecode(tmp_end_time) + "\n")
                translated_text = tmp_str
                if event['createTranscribeJob']['sourceLanguage'] == "en":
                    translated_text = translate_text(tmp_str, "en", "ja")
                fp_ja.write(translated_text + "\n")
                fp_ja.write("\n")
                
                fp_en.write(create_timecode(tmp_start_time) + " --> " + create_timecode(tmp_end_time) + "\n")
                translated_text = tmp_str
                if event['createTranscribeJob']['sourceLanguage'] == "ja":
                    translated_text = translate_text(tmp_str, "ja", "en")
                fp_en.write(translated_text + "\n")
                fp_en.write("\n")
                
                tmp_str = ""
                tmp_start_time = item['start_time']
                init_flag = True
            
            tmp_end_time = item['end_time']
            
        if 'alternatives' in item:
            if event['createTranscribeJob']['sourceLanguage'] == "en" and 'start_time' in item:
                tmp_str = tmp_str + " " + item['alternatives'][0]['content']
            else:
                tmp_str = tmp_str + item['alternatives'][0]['content']
    
    fp_ja.close()
    fp_en.close()
    
    bucket = s3.Bucket(s3bucket)
    caption_file_jp = "vtt/" + event['createTranscribeJob']['jobName'] + '_ja.vtt'
    caption_file_en = "vtt/" + event['createTranscribeJob']['jobName'] + '_en.vtt'
    bucket.upload_file('/tmp/tmp_ja.vtt', caption_file_jp)
    bucket.upload_file('/tmp/tmp_en.vtt', caption_file_en)
    
    os.remove('/tmp/tmp_ja.vtt')
    os.remove('/tmp/tmp_en.vtt')
    
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
        UpdateExpression = "set caption_jp=:cj, caption_en=:ce, new_arrivals=:na",
        ExpressionAttributeValues = {
            ':cj': "https://" + outputDomain + "/" + caption_file_jp,
            ':ce': "https://" + outputDomain + "/" + caption_file_en,
            ':na': 1
        }
    )
    
    return
