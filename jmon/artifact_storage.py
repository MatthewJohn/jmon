
from io import BytesIO

import boto3
import boto3.session
import botocore.exceptions

import jmon.config


class ArtifactStorage:

    def __init__(self):
        """Create client"""
        s3_kwargs = {}
        if endpoint := jmon.config.Config.get().AWS_ENDPOINT:
            s3_kwargs['endpoint_url'] = endpoint
            s3_kwargs['config'] = boto3.session.Config(signature_version='s3v4')
        self._s3_client = boto3.client('s3', **s3_kwargs)
        self._s3_resource = boto3.resource('s3', **s3_kwargs)

    def _get_bucket(self):
        """Get bucket object"""
        return self._s3_resource.Bucket(
            jmon.config.Config.get().AWS_BUCKET_NAME
        )

    def upload_file(self, path, content=None, source_path=None):
        """Upload log to s3"""
        # If a source path is provided, read content from file
        if source_path:
            with open(source_path, 'rb') as fh:
                content = fh.read()

        self._get_bucket().put_object(
            Key=path,
            Body=content
        )

    def list_files(self, path_prefix):
        """List files in path prefix"""
        return [
            file.key
            for file in self._get_bucket().objects.filter(Prefix=path_prefix)
        ]

    def get_file(self, path):
        """Get content for artifact"""
        content = BytesIO()
        try:
            self._get_bucket().download_fileobj(Key=path, Fileobj=content)
        except botocore.exceptions.ClientError:
            return None
        content.seek(0)
        return content.read()
