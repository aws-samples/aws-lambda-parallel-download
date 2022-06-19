# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

from typing import Union

from aws_cdk import (
    Duration,
    aws_lambda as lambda_,
)
from constructs import Construct
from cdk_nag import NagSuppressions, NagPackSuppression


class Function(Construct):
    def __init__(self, scope: Construct, construct_id: str, *,
                 bucket_name: str,
                 max_workers: int = 1000,
                 runtime: lambda_.Runtime = lambda_.Runtime.PYTHON_3_9,
                 memory_size: Union[int, float, None] = 2304,
                 architecture: lambda_.Architecture = lambda_.Architecture.ARM_64,
                 timeout: Duration = Duration.seconds(300),
                 **kwargs):
        super().__init__(scope, construct_id)

        self.lambda_function = lambda_.Function(
          self, construct_id,
          runtime=runtime,
          memory_size=memory_size,
          architecture=architecture,
          timeout=timeout,
          handler="parallel.handler",
          code=lambda_.Code.from_asset("resources"),
          environment={
              "BUCKET": bucket_name,
              "MAX_WORKERS": str(max_workers),
          },
          **kwargs
        )

        NagSuppressions.add_resource_suppressions(
          self.lambda_function.role,
          [
            NagPackSuppression(
              id="AwsSolutions-IAM4",
              reason=("Using the AWSLambdaBasicExecutionRole managed policy to be able to send logs"
                      "to CloudWatch"),
              applies_to=[("Policy::arn:<AWS::Partition>:iam::aws:policy/"
                           "service-role/AWSLambdaBasicExecutionRole")]
            )
          ]
        )
