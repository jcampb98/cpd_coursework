"""
This script is the Lambda function which:
	- Extracts relevant details from the SQS messages
	- Uses image names extracted to call AWS Rekognition PPE Detection 
 	  to analyze the images with the exact names in the S3 Bucket
	- Manipulate the response and prepare the data to send in sms
    - Stores the image labels in the DynamoDB Table 'myDynamoDB2024472-myDynamoDBTable-36G4D3OUD89Z'
    - Sends an SMS to a specified phone number with the Body Parts detected
"""

# imports required resources
import json 
import boto3 
import os
from decimal import Decimal 
# imports code from the "storeDb" file to allow the results from the labeling rekognition to be stored into the dynamodb. 
from store_db import storeDb
# imports code from the "warning" file to enable sms messages to be sent to a phone that is known as '+ZZ-ZZZZZZZZZZ' for demo purposes
from warning import send_message

#low-level client representing Amazon service rekognition
client = boto3.client('rekognition')
    
#used to create a python dictionary for it to be stored in the database
dictionary_labels = dict()
labelsStore = dict()
dictionary_ppe = dict()

def lambda_handler(event, context):
    record = json.loads(event['Records'][0]['body'])
    json_message = json.loads(record['Message'])
    records = json_message['Records'][0]
    
    object_key = records['s3']['object']['key']
    
    bucket_name = records['s3']['bucket']['name']
    
    #Detects instances of real-world entities within an image provided as input.
    dictionary_labels = client.detect_labels(Image={'S3Object':{'Bucket': bucket_name,'Name': object_key}}, MaxLabels=5) #Maximum amount of labels adhering to the brief. 
    
    for label in dictionary_labels['Labels']:
        label_name = label['Name']
        conf = label['Confidence']
        
        conf = Decimal(conf)
        
        labelsStore[label_name] = {"Confidence" : (conf)}

    #Prints dynamo db results 
    print(dictionary_labels)
    # links to the storeDb page
    storeDb(labelsStore, object_key)
    
    dictionary_ppe = client.detect_protective_equipment(Image={'S3Object':{'Bucket': bucket_name,'Name': object_key}},
    SummarizationAttributes={
        'MinConfidence': 0.70,
        'RequiredEquipmentTypes': [
            'FACE_COVER', 'HAND_COVER',
        ]
    })
    
    
    not_wearing = dictionary_ppe['Summary']['PersonsWithoutRequiredEquipment']
    
    indeterminate = dictionary_ppe['Summary']['PersonsIndeterminate']
    
    print(dictionary_ppe)
    
    print(not_wearing)
    # if one of the images is flaged a message will be sent. 
    #if (not_wearing):
        #print("Sending SMS")
        #send_message(object_key)
    #elif(indeterminate):
        #print("Unreconised Equipment")
    #else:
        #print("all good to start working")
        
        

    return {
        'statusCode': 200,
        
    }
