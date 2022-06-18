# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

"""Lambda handler for parallel object download from S3"""

from concurrent.futures import ThreadPoolExecutor
import json
import multiprocessing
import os
import threading

import boto3
import botocore

# Load the environment variables
if "MAX_WORKERS" in os.environ:
    MAX_WORKERS = int(os.environ["MAX_WORKERS"])
else:
    MAX_WORKERS = None

BUCKET_NAME = os.environ["BUCKET"]
OBJECT_KEY = os.environ["OBJECT_KEY"]

# Setup the S3 client
# Sets the max_pool_connections to allow each thread to use the same client
client_config = botocore.config.Config(
    max_pool_connections=MAX_WORKERS
)
client_s3 = boto3.client("s3", config=client_config)


def download_s3(key: str) -> bytes:
    """Download an object from the S3 bucket

    :param key: the key of the object.
    :type key: str
    :returns: the object data
    :rtype: bytes
    """
    obj = client_s3.get_object(Bucket=BUCKET_NAME, Key=key)
    return obj["Body"].read()


def handler(event, context):
    """Read an object from S3 multiple times in parallel.

    The `event` parameter is an object with the following properties:
    * repeat (default 10000): number of times to download the object from S3.

    :param event: an object with the parameters.
    :type event: dict
    :returns: an object with information about the execution.
    :rtype: dict
    """
    if event is None:
        event = {}
    repeat = int(event.get("repeat", "10000"))

    result = {
        "cpu_count": multiprocessing.cpu_count(),
        "threads": {
            "start": threading.active_count()
        },
        "total_reads": 0,
        "total_size": 0,
        "total_records": 0,
    }

    # Download the object `repeat` times
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        for s3_object in executor.map(download_s3, (OBJECT_KEY for _ in range(repeat))):
            result["total_reads"] += 1
            result["total_size"] += len(s3_object)
            data = json.loads(s3_object)
            result["total_records"] += len(data)

        result["threads"]["used"] = threading.active_count()

    return result
