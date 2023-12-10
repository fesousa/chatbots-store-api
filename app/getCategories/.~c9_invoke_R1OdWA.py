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


produtos_categorias= {
    'Bebidas Alcoólicas': ['Cerveja', 'Gin', 'Vinho', 'Vodka', 'Cachaça'],
    'Sucos e Chás':['suco de uva', 'suco de laranja', 'chá verde'],
    'Água': ['com gás', 'sem gás', 'água de coco'],
    'Energéticos':['gatorade', 'redbull', 'powerade']
    
}

def handler(event, context):    
    print(event)
    q = urllib.parse.unquote_plus(event['rawQueryString'].split("=")[1])
    produtos = produtos_categorias[q]
    #retornar informações no campo info, no formato JSON
    return {'statusCode': 200, "body":json.dumps({'produtos':produtos}), "headers": {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "OPTIONS,GET,POST"}}
    
    


    
        
   
