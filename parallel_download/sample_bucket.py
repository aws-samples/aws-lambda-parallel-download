# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

from aws_cdk import (
    RemovalPolicy,
    aws_s3 as s3,
)
from constructs import Construct


class Bucket(Construct):
    def __init__(self, scope: Construct, construct_id: str):
        super().__init__(scope, construct_id)

        self.bucket = s3.Bucket(
            self, construct_id,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            encryption=s3.BucketEncryption.S3_MANAGED,
            enforce_ssl=True,
            server_access_logs_prefix="logs",
            removal_policy=RemovalPolicy.DESTROY,
        )
