import boto3
from pathlib import Path
from app.env_variables import (
    AWS_ACCESS_KEY,
    AWS_SECRET_ACCESS_KEY,
    BUCKET_NAME,
    BUCKET_SUBFOLDER_NAME
)

class FileUploadConfig:

    def __init__(self, request):
        self.aws_access_key_id = AWS_ACCESS_KEY
        self.aws_secret_access_key = AWS_SECRET_ACCESS_KEY
        self.bucket_name = BUCKET_NAME
        self.bucket_subfolder_name = BUCKET_SUBFOLDER_NAME

        self.s3 = boto3.client(
            's3',
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key
        )

        self.file = request.files.get('file')
        self.filename = self.file.filename

    def send_to_aws(self):
        if self.file:
            self.file.save(self.filename)

            s3_response = self.s3.upload_file(
                self.filename,
                self.bucket_name,
                f'{self.bucket_subfolder_name}/{self.filename}'
            )

            Path.cwd().joinpath(self.filename).unlink()

            url = f'https://{self.bucket_name}.s3.eu-central-1.amazonaws.com/{self.bucket_subfolder_name}/{self.filename}'
            return {
                'url': url
            }
