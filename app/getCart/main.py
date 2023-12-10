import json
import traceback
import os
import boto3
import uuid
from decimal import Decimal

from random import randint
from botocore.exceptions import ClientError

# módulos para envio de e-mail
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from boto3.dynamodb.conditions import Key, Attr

class DecimalEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, Decimal):
      return str(obj)
    return json.JSONEncoder.default(self, obj)


def handler(event, context):    
    print(event)
    req = event['queryStringParameters']
    print(req)
    
    dynamodb = boto3.resource('dynamodb')
    cart = dynamodb.Table('cart')
    produtos = dynamodb.Table('products')
    
    cart_items = cart.get_item(
            Key={'email': req['email'], 'cart':req['cart']})
    
    products = cart_items['Item'].get('products',[])
    print(products)
    
    t = 0
    for p in products:
      prod = produtos.query(
        KeyConditionExpression=Key('product').eq(p['item']))
      print(prod)
        
      t = t + prod['Items'][0]['price']*p['q']
    
   
    
    return {'statusCode': 200, "body":json.dumps({'status':'OK', 'produtos':products, 'total': t}, cls=DecimalEncoder), "headers": {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "OPTIONS,POST"}}
    
    


    
        
   
