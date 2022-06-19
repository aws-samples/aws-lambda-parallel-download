# Parallel I/O bound process in AWS Lambda with Python

Sample project to run I/O bound process in AWS Lambda with Python.

This CDK project creates a sample JSON file in an Amazon S3 bucket
that is downloaded in parallel by a Lambda function. The [AWS Lambda
Power Tuning][1].
is also deployed to visualize and fine-tune the memory/power
configuration of Lambda functions.

The parallel download is done using threads through the
[concurrent.futures.ThreadPoolExecutor][2]. The solution is target
Python 3.8 or above as the ThreadPoolExecutor is optimized to reuse
idle worker threads.

For CPU bound process, process should be used instead of threads.

[1]: https://github.com/alexcasalboni/aws-lambda-power-tuning
[2]: https://docs.python.org/3.9/library/concurrent.futures.html#concurrent.futures.ThreadPoolExecutor

## Requirements

* [Python 3.8 or above](https://www.python.org/downloads/)

* [AWS CDK v2](https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html)

* A working AWS account


## Deployment

1. Create a python 3.8+ .venv in the root of repository:
   
   `python3 -m venv .venv`

2. Activate the virtualenv:

   `source .venv/bin/activate`

3. Install the dependencies:

   `pip install -r requirements.txt`

4. Deploy the stack

   `cdk deploy`

5. Upload the sample file

   `aws s3 cp sample.json s3://--ParallelDownloadStack.SampleS3BucketName--`

   Substitute the `--ParallelDownloadStack.SampleS3BucketDomainName--`
   with the value from the CDK output.

## Run the AWS Lambda Power Tuning

At the [Step functions AWS console][3], locate the State machine with
the ARN from the CDK output `ParallelDownloadStack.StateMachineARN`.

At the __Start execution__, use the following JSON:

```
{
  "lambdaARN": "--ParallelDownloadStack.LambdaFunctionARN--",
  "num": 5,
  "payload": {"repeat": 2000, "objectKey": "sample.json"},
  "powerValues": [512,1024,2048,3072,4096,10240]
}
```

Substitute the `--ParallelDownloadStack.LambdaFunctionARN--` with the
value from the CDK output. The `repeat` attribute at the __payload__
is the amount of S3 object download it will perform and the
`objectKey` attribute is the name of the object that will be
downloaded `repeat` times.

New accounts might not be able to configure the Lambda function with
more than 3,008 MB, so you may need to adjust the `powerValues`
property with a list of memory values below this limit, if this is
your case.

When the execution ends, you can get the URL with the results from
the __Execution input & output__ tab, property
`stateMachine.visualization`.

[3]: https://console.aws.amazon.com/states/home