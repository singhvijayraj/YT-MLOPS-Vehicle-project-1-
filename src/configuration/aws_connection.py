import boto3
import os
from dotenv import load_dotenv
from pathlib import Path

class S3Client:
    def __init__(self, env_file: str):
        # Load environment variables
        env_path = Path(env_file)
        if not env_path.exists():
            raise FileNotFoundError(f"Environment file not found: {env_path}")

        load_dotenv(env_path)

        # Get credentials from env
        access_key = os.getenv('AWS_ACCESS_KEY_ID')
        secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        endpoint_url = os.getenv('AWS_ENDPOINT_URL')
        region_name = os.getenv('AWS_DEFAULT_REGION')

        if not all([access_key, secret_key, endpoint_url, region_name]):
            raise ValueError("Missing one or more required environment variables.")

        # Create S3 client
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region_name,
            endpoint_url=endpoint_url
        )

# Usage
# if __name__ == "__main__":
#     env_file_path = r"D:\ai_engeering roadmap\MLops\git tutorial\proj1-Vehical-insurance\YT-MLOPS-Vehicle-project-1-\src\configuration\aws.env"
#     client = S3Client(env_file_path)

#     bucket_name = os.getenv("B2_BUCKET")
#     file_to_upload = r"D:\ai_engeering roadmap\MLops\git tutorial\proj1-Vehical-insurance\YT-MLOPS-Vehicle-project-1-\projectfolw.txt"  # replace with actual file

#     client.s3_client.upload_file(
#         Filename=file_to_upload,
#         Bucket=bucket_name,
#         Key="test.txt"
#     )

#     print("Uploaded test.txt ✅")