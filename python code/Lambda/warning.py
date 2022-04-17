#This page is imported to the lambda function page
# imports required resources 

import boto3
import os
import json 

sns = boto3.client('sns')

def send_message(object_key):
    
    number = 'ZZ-ZZZZZZZ'

    message = " is not wearing correct PPE"
    
    message = object_key + message
        
    sns.publish(PhoneNumber = number, Message = message)
    
    print("sms has sent")
