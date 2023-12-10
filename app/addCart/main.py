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
    
    cart_items = cart.get_item(
            Key={'email': req['email'], 'cart':req['cart']})
    
    products = cart_items['Item'].get('products',[])
    
    products.append({'item': req['item'], 'q': req['q']})
            
    response = cart.update_item(
        Key={
            'email' : req['email'],
            'cart': req['cart']
        },
        UpdateExpression="set products=:products",
        ExpressionAttributeValues={':products': products},
        ReturnValues="UPDATED_NEW"
    )
    
    return {'statusCode': 200, "body":json.dumps({'status':'OK'}), "headers": {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "OPTIONS,POST"}}
    
    


    
        
   
