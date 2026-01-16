import boto3
import os
from dotenv import load_dotenv

load_dotenv()

sts = boto3.client(
    "sts",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)

identity = sts.get_caller_identity()

print("AWS connection successful")
print("Account ID:", identity["Account"])
print("IAM User ARN:", identity["Arn"])
