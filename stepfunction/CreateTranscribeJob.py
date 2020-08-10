import json
import boto3
import uuid

transcribe = boto3.client('transcribe')

def lambda_handler(event, context):
    jobName = str(uuid.uuid4())
    targetBucket = event['OutputBucket']
    response = transcribe.start_transcription_job(
        TranscriptionJobName=jobName,
        LanguageCode = event['LanguageCode'],
        Media={
            'MediaFileUri': event['MediaFileURL']
        },
        OutputBucketName=targetBucket
    )
    sourceLanguage = event['LanguageCode'].split('-')[0]
    return {
        'jobName': jobName,
        'outputBucketName': targetBucket,
        'sourceLanguage': sourceLanguage
    }
