from . lambdafunction import LambdaFunction


def update_function_code(code_pipeline_job):
    function_name = code_pipeline_job.params['function_name']
    print(f'Function name passed in user parameters: {function_name}')

    artifact_name = code_pipeline_job.params['artifact_name']
    print(f'Artifact name passed in user parameters: {artifact_name}')

    artifact_data = code_pipeline_job.find_artifact(artifact_name)
    print(f'Retrieved information about the artifact {artifact_name}')

    bucket = artifact_data['location']['s3Location']['bucketName']
    print(f'Identified artifact {artifact_name} is in S3 bucket: {bucket}')

    key = artifact_data['location']['s3Location']['objectKey']
    print(f'Identified the S3 key for artifact {artifact_name} is: {key}')

    lambda_function = LambdaFunction(function_name)
    print(f'Created a Lambda function client for function with name: {function_name}')

    update_function_return = lambda_function.update_function_code(bucket, key)
    print(f'Updated code of Lamdbda function with name: {function_name}')

    version_publish_return = lambda_function.publish_version(update_function_return['CodeSha256'])
    print(f'Published new Lamdbda function version: {version_publish_return["Version"]}')

    alias_name = code_pipeline_job.params['alias_name']
    print(f'Alias name passed in user parameters: {alias_name}')

    update_alias_return = lambda_function.update_alias(alias_name, version_publish_return["Version"])
    print(f'Updated alias of Lamdbda function with name: {alias_name} to version: {version_publish_return["Version"]}')

    code_pipeline_job.put_job_success(f'Successfully updated Lamdbda function with name: {function_name}')
