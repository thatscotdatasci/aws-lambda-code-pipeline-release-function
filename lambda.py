from releasefunction import releasefunction
from releasefunction.codepipelinejob import CodePipelineJob


def lamdba_handler(event, context):
    code_pipeline_job = CodePipelineJob(event)
    print(f'Job ID: {code_pipeline_job.id}')

    try:
        releasefunction.update_function_code(code_pipeline_job)
        return "Complete"
    except Exception as e:
        print(f'Updating Lambda function failed due to exception: {str(e)}')
        code_pipeline_job.put_job_failure(f'Function exception: {str(e)}')
