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
    

    u = os.getenv('USERMAIL')
    g = os.getenv('PWDMAIL')
    
    t = randint(10000, 99999)
    
    try:
         # configuração e envio de email
        message = MIMEMultipart()
        message['From'] = u
        message['To'] = req['email']
        message['Subject'] = 'Pedido confirmado'
        texto_mensagem = f'<h1>Seu pedido {t} está confirmado!</h1>'
        message.attach(MIMEText(texto_mensagem, 'html'))
        
        session = smtplib.SMTP(os.getenv("SERVERMAIL"), os.getenv("PORTMAIL")) 
        session.starttls()
        session.login(u, g)
        text = message.as_string()
        session.sendmail(u, req['email'], text)
        session.quit()
        
        r = {"mensagem": "E-mail de confirmação enviado", "status": "OK"}
         
    except Exception as ex:
        print(traceback.print_exc())
        # retorno de erro no formato JSON
        r = {"status":"ERRO",'mensagem':'Erro ao enviar e-mail'}
            
        
        
    
    return {'statusCode': 200, "body":json.dumps(r), "headers": {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "OPTIONS,POST"}}
    
    


    
        
   
