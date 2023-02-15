
import boto3
import boto3.session

import jmon.config


class Storage:

    def __init__(self):
        """Create client"""
        s3_kwargs = {}
        if endpoint := jmon.config.Config.get().AWS_ENDPOINT:
            s3_kwargs['endpoint_url'] = endpoint
            s3_kwargs['config'] = boto3.session.Config(signature_version='s3v4')
        self._s3 = boto3.client('s3', **s3_kwargs)

    def upload_file(self, path, content):
        """Upload log to s3"""
        self._s3.put_object(
            Bucket=jmon.config.Config.get().AWS_BUCKET_NAME,
            Key=path,
            Body=content
        )
