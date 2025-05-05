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
s3.put_object(Bucket='blogapi-pyronlab', Key='testfile.txt', Body='Hello World')

# import os
# import django

# # Set up Django settings
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blogapi.settings")  # Replace with your actual project name
# django.setup()

# from django.core.files.storage import default_storage
# from django.core.files.base import ContentFile

# default_storage.save("test_upload.txt", ContentFile(b"Hello S3"))
