# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

from aws_cdk import (
    CfnOutput,
    Stack,
    aws_iam as iam,
)
from constructs import Construct
from cdk_nag import NagSuppressions, NagPackSuppression

from . import sample_bucket, parallel_lambda, powertuning


class ParallelDownloadStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        sample = sample_bucket.Bucket(self, "SampleBucket")
        CfnOutput(
            self, "SampleS3BucketName",
            value=sample.bucket.bucket_name,
        )

        lambda_fn = parallel_lambda.Function(
            self, "ParallelLambda",
            bucket_name=sample.bucket.bucket_name
        )

        lambda_fn.lambda_function.role.add_to_principal_policy(iam.PolicyStatement(
            actions=["s3:GetObject"],
            resources=[sample.bucket.arn_for_objects("*")],
        ))
        NagSuppressions.add_resource_suppressions_by_path(
            self,
            f"{lambda_fn.lambda_function.role.node.path}/DefaultPolicy/Resource",
            [
                NagPackSuppression(
                    id="AwsSolutions-IAM5",
                    reason=("The user can upload any object to the bucket, so the resource needs"
                            "wildcard"),
                    applies_to=[
                        f"Resource::<{self.get_logical_id(sample.bucket.node.default_child)}.Arn>/*"
                    ]
                )
            ]
        )
        CfnOutput(
            self, "LambdaFunctionARN",
            value=lambda_fn.lambda_function.function_arn,
        )

        tuning = powertuning.PowerTuning(
            self, "PowerTuning",
            function_arn=lambda_fn.lambda_function.function_arn
        )
        CfnOutput(
            self, "StateMachineARN",
            value=tuning.sam.get_att("Outputs.StateMachineARN").to_string()
        )
