# This page is imported to the lambda function page

# imports required resources

import boto3

dynamodb = boto3.client('dynamodb')

def storeDynamo (dictionary, object_key):
    
    labels = []
    
    for key in dictionary:
        
        info = "Label: " + key + ", Confidence: " + str(dictionary[key]['Confidence'])
        
        labels.append(info)
        
    dynamodb.put_item(TableName='DynamoDBs2032103-myDynamoDBTable-G0I7ZMX8PJSB',
    Item = {
        #Set to the partition key from the dynamo table
        "Name": {"S": object_key}, 
        "Labels":{"SS": labels}
        
    })
   
    print("The Items are stored into the Dynamo Database")