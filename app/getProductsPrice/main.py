import json
import traceback
import os
import boto3
import uuid
from decimal import Decimal

from random import randint
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr

# módulos para envio de e-mail
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


produtos_categorias= {
    'Bebidas Alcoólicas': ['Cerveja', 'Gin', 'Vinho', 'Vodka', 'Cachaça'],
    'Sucos e Chás':['suco de uva', 'suco de laranja', 'chá verde'],
    'Água': ['com gás', 'sem gás', 'água de coco'],
    'Energéticos':['gatorade', 'redbull', 'powerade']
    
}

class DecimalEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, Decimal):
      return str(obj)
    return json.JSONEncoder.default(self, obj)

def handler(event, context):    
    print(event)
    q = event['queryStringParameters']['categoria']
    
    dynamodb = boto3.resource('dynamodb')
    products = dynamodb.Table('products')
    p = products.scan(
        FilterExpression=Attr('category').eq(q)
    )
    print(p)
    
    #produtos = produtos_categorias[q]
    produtos = p['Items']
    #retornar informações no campo info, no formato JSON
    return {'statusCode': 200, "body":json.dumps({'produtos':produtos}, cls=DecimalEncoder), "headers": {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "OPTIONS,GET,POST"}}
    
    


    
        
   
