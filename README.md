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

## Run the AWS Lambda Power Tuning

At the [Step functions AWS console][3], locate the State machine with
the ARN from the CDK output `ParallelDownloadStack.StateMachineARN`.

At the __Start execution__, use the following JSON:

```
{
  "lambdaARN": "--ParallelDownloadStack.LambdaFunctionARN--",
  "num": 5,
  "payload": {"repeat": 2000}
}
```

Substitute the `--ParallelDownloadStack.LambdaFunctionARN--` with the
value from the CDK output. The `repeat` attribute at the __payload__
is the amount of S3 object download it will perform.

[3]: https://console.aws.amazon.com/states/home

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

