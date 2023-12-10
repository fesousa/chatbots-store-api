import json
import traceback
import os
import boto3

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
    users = dynamodb.Table('users')
    r = ""
    try:
        response = users.get_item(
            Key={'email': req['email']})
    except ClientError as e:
        r = {"status":"ERRO",'mensagem':'Usuário não encontrado'}
    else:
        print(response)
        token_db = response['Item']['token_code']
        
        if token_db ==  req['token']:
            
            r = {"mensagem": "Usuário autenticado", "status": "OK"}
             
        else:
            r = {"status":"ERRO",'mensagem':'Erro ao verificar usuário'}
            
        
        
    
    return {'statusCode': 200, "body":json.dumps(r), "headers": {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "OPTIONS,POST"}}
    
    


    
        
   
