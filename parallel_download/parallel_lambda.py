# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

from typing import Union

from aws_cdk import (
    Duration,
    RemovalPolicy,
    Stack,
    aws_lambda as lambda_,
    aws_logs as logs,
    aws_iam as iam,
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

        role = iam.Role(
          self, "LambdaExecution",
          assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
        )

        policy = iam.PolicyStatement(
          actions=["logs:CreateLogStream", "logs:PutLogEvents"],
          resources=["*"],
        )

        role.add_to_policy(policy)

        self.lambda_function = lambda_.Function(
          self, construct_id,
          runtime=runtime,
          memory_size=memory_size,
          architecture=architecture,
          timeout=timeout,
          handler="parallel.handler",
          code=lambda_.Code.from_asset("resources"),
          role=role,
          environment={
              "BUCKET": bucket_name,
              "MAX_WORKERS": str(max_workers),
          },
          **kwargs
        )

        logs.LogGroup(
          self, f"loggroup-{construct_id}",
          log_group_name=f"/aws/lambda/{self.lambda_function.function_name}",
          removal_policy=RemovalPolicy.DESTROY,
          retention=logs.RetentionDays.ONE_DAY,
        )

        NagSuppressions.add_resource_suppressions_by_path(
          Stack.of(self),
          "/ParallelDownloadStack/ParallelLambda/LambdaExecution/DefaultPolicy/Resource",
          [
            NagPackSuppression(
              id="AwsSolutions-IAM5",
              reason=("The Lambda function name is unknown before deployment, so wildcard needs to"
                      "be used to give access to CloudWatch"),
              applies_to=[("Resource::*")]
            )
          ]
        )
