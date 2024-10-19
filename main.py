
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, jsonify, request
from dotenv import load_dotenv

load_dotenv()

app= Flask(__name__)

def send_email(subject, email, body):
    #variables env 
    email_sender=os.getenv("GoogleMail__Emailsender")
    email_password=os.getenv("GoogleMail__ApiKey") 
    smtp_server=os.getenv("GoogleMail__Host")
    smpt_port=os.getenv("GoogleMail__Port") 
    
    #mensaje
    msg= MIMEMultipart()
    msg['From'] = email_sender
    msg['To'] = email
    msg['Subject'] = subject

    #cuerpo
    msg.attach(MIMEText(body, 'html'))

    try:
        with smtplib.SMTP(smtp_server, int(smpt_port)) as server:
            server.starttls()
            server.login(email_sender, email_password)
            server.sendmail(email_sender,email, msg.as_string())
        return True
    except Exception as e:
        return False ,str(e)
    
@app.route('/send-email', methods=['POST'])
def send_email_endponit():
    data= request.json
    subject= data.get('subject')
    recipient= data.get('recipient')
    body_html= data.get('body_html')

    succes= send_email(subject, recipient, body_html)
    print(succes)
    if succes:
        return jsonify({'message':'email send succesfully'})
    else:
        return jsonify({'message': f'failed to send email'})
    
if __name__ == "__main__":
    app.run(debug= True)



        