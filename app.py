#!/usr/bin/env python3
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import aws_cdk as cdk
import cdk_nag

from parallel_download.parallel_download_stack import ParallelDownloadStack


app = cdk.App()
cdk.Aspects.of(app).add(cdk_nag.AwsSolutionsChecks(verbose=True))
ParallelDownloadStack(app, "ParallelDownloadStack")

app.synth()
