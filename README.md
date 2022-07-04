# Parallel dowload from Amazon S3 using Lambda function

Sample code to parallel read objects from Amazon S3 buckets which
showcases how to efficiently run I/O bound tasks using AWS Lambda
functions using Python.

For I/O bound tasks, you can use multiple threads. In this sample
code, the concurrent.futures.ThreadPoolExecutor is used with a 1,000
maximum simultaneous threads. Lambda functions allow up to 1,024
threads, and you should consider that 1 thread is your main process.
You also need to increase the max pool connections in botocore so all
threads can execute the S3 object download simultaneously.

The sample code uses one 8.3 KB object at S3 with JSON data read 
multiple times. After reading the object, it is decoded from JSON to 
Python object. The result after running this sample was 1,000 reads 
processed in 3 seconds and 10,000 reads processed in 25 seconds using 
a Lambda configured with 2,304 MB. Increasing the Lambda memory didn't 
help to decrease the time to run the task.​

The code in this repository helps you set up the following target
architecture.

![Target architecture diagram](architecture.png "Architecture image")​

For prerequisites and instructions for using this AWS Prescriptive
Guidance pattern, see [Parallel reading from S3 in Lambda](https://apg-library.amazonaws.com/content/b46e9b16-9842-4291-adfa-3ef012b89aec). 