# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

from aws_cdk import (
    # Duration,
    CfnOutput,
    Stack,
    # aws_sqs as sqs,
)
from constructs import Construct

from . import sample_bucket, parallel_lambda, powertuning


class ParallelDownloadStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        sample = sample_bucket.Bucket(self, "SampleBucket", sample_repeat=43)
        lambda_fn = parallel_lambda.Function(self, "ParallelLambda",
            bucket_name=sample.bucket.bucket_name, object_key=sample.object_key)
        sample.bucket.grant_read(lambda_fn.lambda_function)

        CfnOutput(self, "LambdaFunctionARN",
            value=lambda_fn.lambda_function.function_arn,
        ) 

        tuning = powertuning.PowerTuning(self, "PowerTuning",
            function_arn=lambda_fn.lambda_function.function_arn
        )
        CfnOutput(self, "StateMachineARN",
            value=tuning.sam.get_att("Outputs.StateMachineARN").to_string()
        )
        
