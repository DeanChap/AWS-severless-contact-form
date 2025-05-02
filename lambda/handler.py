import boto3
import os
import json

def lambda_handler(event, context):
    ses = boto3.client('ses', region_name='ca-central-1')

    try:
        body = json.loads(event['body'])

        name = body.get('name')
        email = body.get('email')
        message = body.get('message')

        email_body = f"New contact form submission:\n\nName: {name}\nEmail: {email}\nMessage:\n{message}"

        response = ses.send_email(
            Source=os.environ['EMAIL_FROM'],
            Destination={
                'ToAddresses': [
                    os.environ['EMAIL_TO'],
                ]
            },
            Message={
                'Subject': {
                    'Data': 'New Contact Form Submission'
                },
                'Body': {
                    'Text': {
                        'Data': email_body
                    }
                }
            }
        )
        return {
            'statusCode': 200,
            'body': 'Email sent successfully!'
        }
    except Exception as e:
        print("SES send_email error:", e)
        return {
            'statusCode': 500,
            'body': 'Failed to send email.'
        }
