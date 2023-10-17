# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

from aws_cdk import (
    aws_sam as sam,
)
from constructs import Construct


class PowerTuning(Construct):
    def __init__(self, scope: Construct, construct_id: str, *, function_arn: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        self.sam = sam.CfnApplication(
            self, 'powerTuner',
            location=sam.CfnApplication.ApplicationLocationProperty(
                application_id=('arn:aws:serverlessrepo:us-east-1:451282441545:'
                                'applications/aws-lambda-power-tuning'),
                semantic_version='4.3.2',
            ),
            parameters={
                "lambdaResource": f"{function_arn}*",
                "PowerValues": "512,1024,2048,3072,4096,10240"
            },
        )
