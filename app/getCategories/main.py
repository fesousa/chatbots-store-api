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


categorias= [
    'Bebidas Alcoólicas',
    'Sucos e Chás',
    'Água',
    'Energéticos']

def handler(event, context):    
    print(event)
    #retornar informações no campo info, no formato JSON
    return {'statusCode': 200, "body":json.dumps({'categorias':categorias}), "headers": {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "OPTIONS,GET,POST"}}
    
    


    
        
   
