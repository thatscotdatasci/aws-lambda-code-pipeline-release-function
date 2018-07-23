import boto3


class LambdaFunction(object):

    def __init__(self, name):
        self._name = name
        self._lambda_function = boto3.client('lambda')

    @property
    def name(self):
        return self._name

    @property
    def function(self):
        return self._lambda_function

    def update_function_code(self, s3_bucket, s3_key):
        """Update the Lambda function code

        Args:
            s3_bucket: The S3 bucket containing the new function code
            s3_key: The key of the function code in the S3 bucket

        Raises:
            Exception: Any exception thrown by .update_function_code(()

        """
        return self._lambda_function.update_function_code(
            FunctionName=self._name,
            S3Bucket=s3_bucket,
            S3Key=s3_key
        )
