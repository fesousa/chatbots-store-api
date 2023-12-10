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
        
        u = os.getenv('USERMAIL')
        g = os.getenv('PWDMAIL')
        
        t = randint(1000, 9999)
        response_tokens = users.update_item(
            Key={
                'email' : response['Item']['email'],
            },
            UpdateExpression="set token_code=:token_code",
            ExpressionAttributeValues={':token_code': t},
            ReturnValues="UPDATED_NEW"
        )
        try:
             # configuração e envio de email
            message = MIMEMultipart()
            message['From'] = u
            message['To'] = response['Item']['email']
            message['Subject'] = 'Código para login'
            texto_mensagem = f'<h1>Seu código para login: {t}</h1>'
            message.attach(MIMEText(texto_mensagem, 'html'))
            
            session = smtplib.SMTP(os.getenv("SERVERMAIL"), os.getenv("PORTMAIL")) 
            session.starttls()
            session.login(u, g)
            text = message.as_string()
            session.sendmail(u, response['Item']['email'], text)
            session.quit()
            
            r = {"mensagem": "Código de acesso enviado por e-mail", "status": "OK"}
             
        except Exception as ex:
            print(traceback.print_exc())
            # retorno de erro no formato JSON
            r = {"status":"ERRO",'mensagem':'Erro ao verificar usuário'}
            
        
        
    
    return {'statusCode': 200, "body":json.dumps(r), "headers": {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "OPTIONS,POST"}}
    
    


    
        
   
