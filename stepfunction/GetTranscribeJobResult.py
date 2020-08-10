import boto3
import json

transcribe = boto3.client('transcribe')

def lambda_handler(event, context):
    jobName = event['createTranscribeJob']['jobName']
    response = transcribe.get_transcription_job(
        TranscriptionJobName=jobName
    )
    
    if response["TranscriptionJob"]["TranscriptionJobStatus"] == "COMPLETED":
        s3infos = response["TranscriptionJob"]["Transcript"]["TranscriptFileUri"].split('/', 4)
        return {
            "result": True,
            "outputS3bucket": s3infos[3],
            "outputS3key": s3infos[4]
        }
        
    return {
        "result": False
    }
