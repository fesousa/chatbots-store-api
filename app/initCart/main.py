import json
import traceback
import os
import boto3
import uuid

from random import randint
from botocore.exceptions import ClientError

# módulos para envio de e-mail
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def handler(event, context):    
    req = json.loads(event['body'])
    print(req)
    
    dynamodb = boto3.resource('dynamodb')
    cart = dynamodb.Table('cart')
        
        
    cart_session = str(uuid.uuid4())
    response = cart.put_item(
        Item={
            "email": req['email'],
            "cart": cart_session
        }
    )
    
    return {'statusCode': 200, "body":json.dumps({'cart':cart_session}), "headers": {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "OPTIONS,POST"}}
    
    


    
        
   
