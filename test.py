import psycopg2
from datetime import datetime, timezone
import json
import boto3
import base64

client = boto3.client('sqs', region_name='us-east-1', endpoint_url='http://localhost:4566')
queue_url='http://localhost:4566/000000000000/login-queue'
cursor = None
conn = None

class Message:
    def __init__(self, user_id, app_version, device_type, ip, locale, device_id, dt):
        self.user_id = user_id
        self.app_version = app_version
        self.device_type = device_type
        self.ip = ip
        self.locale = locale
        self.device_id = device_id
        self.dt = dt
        

class DataTransform:
    def insertUserLoginData(self, messageObject):
        #Executing insert statement using the execute() method
        global conn
        global cursor
        sql = """INSERT INTO user_logins(user_id, device_type, masked_ip, masked_device_id, locale, app_version, create_date)
                    VALUES(%s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(sql, (messageObject.user_id, messageObject.device_type, messageObject.ip, 
        messageObject.device_id, messageObject.locale, messageObject.app_version, messageObject.dt))

        conn.commit()

    def receive_message(self):
            response = client.receive_message(
                QueueUrl=queue_url,
                AttributeNames=['All'],
                MaxNumberOfMessages=100,
                MessageAttributeNames=['All'],
                VisibilityTimeout=2,
                WaitTimeSeconds=100
            )

            message = response['Messages'][0]
            msgBody = json.loads(message['Body'])
            print(msgBody)

            # Handling erroneous data
            if not "user_id" in msgBody:
                self.deleteLastMessage(message)
                return
            
            user_id = msgBody['user_id']
            app_version = msgBody['app_version']
            app_version = int(app_version.replace(".", ""))            
            device_type = msgBody['device_type']

            # Masking by using Base64 encoding ip address
            ip = msgBody['ip']
            ip = base64.b64encode(ip.encode('ascii'))              
            
            # Masking by using Base64 encoding device_id
            device_id = msgBody['device_id']
            device_id = base64.b64encode(device_id.encode('ascii'))

            locale = msgBody['locale']
            dt = datetime.now(timezone.utc)

            messageObject = Message(user_id, app_version, device_type, ip, locale, device_id, dt)
            
            self.insertUserLoginData(messageObject)
            self.deleteLastMessage(message)
            

    def deleteLastMessage(self, message):
        client.delete_message(
                        QueueUrl=queue_url,
                        ReceiptHandle= message['ReceiptHandle']
                    )

    def initializePostgres(self):    
        #establishing the connection
        global conn
        global cursor
        conn = psycopg2.connect(
            database="postgres", user='postgres', password='postgres', host='127.0.0.1', port= '5432'
        )
        #Creating a cursor object using the cursor() method
        cursor = conn.cursor()
        self.startReceiveFromSQS()

    def closePostgresConnection(self):
        #Closing the connection
        global conn
        conn.close()
    
    def startReceiveFromSQS(self):
        # Assuming continous output from SQS
        while True:    
            self.receive_message()
        self.closePostgresConnection()


DataTransform().initializePostgres()
    