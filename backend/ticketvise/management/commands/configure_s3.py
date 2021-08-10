import json

import boto3
from botocore.config import Config
from botocore.exceptions import EndpointConnectionError
from django.core.management.base import BaseCommand

from ticketvise import settings


class Command(BaseCommand):
    """Django command that waits and configures"""

    def handle(self, *args, **options):
        # Create a bucket policy
        # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-example-bucket-policies.html
        download_only_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": [
                        "s3:GetObject"
                    ],
                    "Effect": "Allow",
                    "Resource": [
                        f"arn:aws:s3:::{settings.AWS_STORAGE_BUCKET_NAME}/*"
                    ],
                    "Sid": "AddPerm",
                    "Principal": '*'
                }]
        }

        # Convert the policy from JSON dict to string
        download_only_policy = json.dumps(download_only_policy)

        # Connect to the bucket and set the new policy
        tries_left = 10
        while tries_left > 0:
            try:
                s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                  aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                                  endpoint_url=settings.AWS_S3_ENDPOINT_URL,
                                  config=Config(signature_version='s3v4'))
                s3.put_bucket_policy(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Policy=download_only_policy)
            except EndpointConnectionError:
                print(f"Could not connect to the bucket '{settings.AWS_STORAGE_BUCKET_NAME}' on endpoint URL: '{settings.AWS_S3_ENDPOINT_URL}', retrying {tries_left} more times")
            tries_left -= 1

        if tries_left > 0:
            print(f"Succesfully set policy for Bucket '{settings.AWS_STORAGE_BUCKET_NAME}'!")
        else:
            print(f"Could not connect to the endpoint URL: '{settings.AWS_S3_ENDPOINT_URL}'")
