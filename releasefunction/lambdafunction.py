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

    def publish_version(self, code_sha_256):
        """Publishes a version of the lambda function from the current snapshot of $LATEST

        Args:
            code_sha_256: The SHA256 hash of the deployment package to be published

        Raises:
            Exception: Any exception thrown by .publish_version(()

        """
        return self._lambda_function.publish_version(
            FunctionName=self._name,
            CodeSha256=code_sha_256
        )

    def update_alias(self, alias_name, function_version):
        """Updates the Lambda function version to which the given alias points

        Args:
            alias_name: The alias name
            function_version: The Lambda function version which the alias should point to

        Raises:
            Exception: Any exception thrown by .update_alias(()

        """
        return self._lambda_function.update_alias(
            FunctionName=self._name,
            Name=alias_name,
            FunctionVersion=function_version
        )
