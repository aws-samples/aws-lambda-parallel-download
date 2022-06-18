# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

from aws_cdk import (
    aws_s3 as s3,
    aws_s3_deployment as s3_deployment,
)
from constructs import Construct

# From RFC 8259
SAMPLE_JSON_OBJECT = {
    "Image": {
        "Width":  800,
        "Height": 600,
        "Title":  "View from 15th Floor",
        "Thumbnail": {
            "Url":    "http://www.example.com/image/481989943",
            "Height": 125,
                  "Width":  100
        },
        "Animated": False,
        "IDs": [116, 943, 234, 38793]
    }
}

class Bucket(Construct):
    def __init__(self, scope: Construct, construct_id: str, *, object_key: str =
                 "sample.json", sample_repeat: int = 1):
        super().__init__(scope, construct_id)

        self.bucket = s3.Bucket(self, construct_id)
        self.object_key = object_key

        s3_deployment.BucketDeployment(self, f"{construct_id}Deployment",
            destination_bucket=self.bucket,
            sources=[s3_deployment.Source.json_data(
                self.object_key, [SAMPLE_JSON_OBJECT] * sample_repeat
            )],
        )
