import os
import boto3
from dotenv import load_dotenv

load_dotenv()

session = boto3.Session(
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)

s3 = session.client('s3')
print(os.getenv("AWS_ACCESS_KEY_ID"))
# Test upload
s3.put_object(Bucket='blog-api-pyronlab', Key='testfile.txt', Body='Hello World! Checking s3 uploading')
