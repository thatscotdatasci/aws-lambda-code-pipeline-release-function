import json

from boto3 import client


class CodePipelineJob(object):

    def __init__(self, event):
        self._client = client('codepipeline')
        self._id = event['CodePipeline.job']['id']
        self._job_data = event['CodePipeline.job']['data']
        self._params = self._get_user_params()
        self._artifacts = self._get_artifacts()

    @property
    def id(self):
        return self._id

    @property
    def params(self):
        return self._params

    def find_artifact(self, name):
        """Finds the artifact with 'name' among all of the 'artifacts' passed by the CodePipeline

        Args:
            name: The name of the artifact that we want to find
        Returns:
            The artifact dictionary found
        Raises:
            Exception: If no matching artifact is found

        """
        for artifact in self._artifacts:
            if artifact['name'] == name:
                return artifact

        raise Exception(f'Input artifact named "{name}" not found')

    def _get_user_params(self):
        """Decodes the JSON user parameters and validates the required properties

        Returns:
            The JSON parameters decoded as a dictionary

        Raises:
            Exception: The JSON can't be decoded or a property is missing

        """
        try:
            # Get the user parameters which contain the stack, artifact and file settings
            user_parameters = self._job_data['actionConfiguration']['configuration']['UserParameters']
            decoded_parameters = json.loads(user_parameters)

        except Exception:
            # We're expecting the user parameters to be encoded as JSON so we can pass multiple values.
            # If the JSON can't be decoded then fail the job with a helpful message.
            raise Exception('UserParameters could not be decoded as JSON')

        if 'function_name' not in decoded_parameters:
            # Validate that the function name is provided, otherwise fail the job with a helpful message.
            raise Exception('Your UserParameters JSON must include the name of the Lambda function to be updated')

        if 'artifact_name' not in decoded_parameters:
            # Validate that the artifact name is provided, otherwise fail the job with a helpful message.
            raise Exception('Your UserParameters JSON must include the name of the artifact containing the function '
                            'code that the Lambda function should be updated to')

        return decoded_parameters

    def _get_artifacts(self):
        """Returns a list of all the artifacts passed by the CodePipeline

            Returns:
                List of all the artifacts passed by the CodePipeline

            Raises:
                Exception: No inputArtifacts element present in the data provided by the CodePipeline

            """
        if 'inputArtifacts' not in self._job_data:
            # Validate that input artifacts were passed by the CodePipeline.
            raise Exception('It appears that no artifacts were passed by the CodePipeline')

        return self._job_data['inputArtifacts']

    def put_job_success(self, message):
        """Notify CodePipeline of a successful job

        Args:
            message: A message to be logged relating to the job status

        Raises:
            Exception: Any exception thrown by .put_job_success_result()

        """
        print('Putting job success')
        print(message)
        self._client.put_job_success_result(jobId=self._id)

    def put_job_failure(self, message):
        """Notify CodePipeline of a failed job.

        Args:
            message: A message to be logged relating to the job status

        Raises:
            Exception: Any exception thrown by .put_job_failure_result()

        """
        print('Putting job failure')
        print(message)
        self._client.put_job_failure_result(jobId=self._id, failureDetails={'message': message, 'type': 'JobFailed'})
