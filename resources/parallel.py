# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

from concurrent.futures import ThreadPoolExecutor
import json
import multiprocessing
import os
import threading
import time

import boto3
import botocore

# Load the environment variables
if "MAX_WORKERS" in os.environ:
    MAX_WORKERS = int(os.environ["MAX_WORKERS"])
else:
    MAX_WORKERS = None

BUCKET_NAME = os.environ["BUCKET"]

# Setup the S3 client
# Sets the max_pool_connections to allow each thread to use the same client
client_config = botocore.config.Config(
    max_pool_connections=MAX_WORKERS
)
client_s3 = boto3.client("s3", config=client_config)


def download_s3(key: str) -> bytes:
    """Download an object from the S3 bucket"""
    obj = client_s3.get_object(Bucket=BUCKET_NAME, Key=key)
    return obj["Body"].read()


def handler(event, context):
    """Read an object from S3 multiple times in parallel.

    The `event` parameter is an object with the following properties:
    * repeat (default 10000): number of times to download the object from S3.
    * objectKey: the object key to download in parallel
    """
    repeat = int(event.get("repeat", 10000))
    object_key = event["objectKey"]

    print("CPU count:", multiprocessing.cpu_count())
    print("threads in use at start:", threading.active_count())

    total_reads = 0
    total_size_read = 0
    total_records_read = 0
    total_time = None

    # Download the object `repeat` times
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        start = time.perf_counter()

        for s3_object in executor.map(download_s3, (object_key for _ in range(repeat))):
            total_reads += 1
            total_size_read += len(s3_object)
            data = json.loads(s3_object)
            total_records_read += len(data)

        total_time = time.perf_counter() - start

        print("total threads used:", threading.active_count())

    return {
        "objects_read": total_reads,
        "bytes_read": total_size_read,
        "time_sec": total_time,
        "objects_per_sec": round(total_reads/total_time),
        "bytes_per_sec": round(total_size_read/total_time),
    }
