# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [1.2.0] - 2025-01-02
### Changed
- Changed the max workers to 30 at the Lambda function for better
  resource utilization.
- Updated the default Lambda function memory to 2304 due new tests. 
- aws-cdk-lib version bumped to 2.173.4.
- cdk-nag version bumped to 2.34.23.
- Lambda function runtime to Python 3.13.
- Power Tuning version bumped to 4.3.6.

### Fixed
- Added the public_read_access False to the S3 bucket.
- Removed .venv from flake8 analysis.

## [1.1.2] - 2024-02-02
### Changed
- aws-cdk-lib version bumped to 2.101.1.
- cdk-nag version bumped to 2.28.27.
- Lambda function runtime changed to Python 3.12.
- Power Tuning version bumped to 4.3.3.

## [1.1.1] - 2023-10-16
### Changed
- aws-cdk-lib version bumped to 2.126.0.
- cdk-nag version bumped to 2.27.64.
- Lambda function runtime changed to Python 3.11.
- Power Tuning version bumped to 4.3.2.
- Updated cdk.json to the definition set on cdk 2.101.1.
- Updated the Lambda function memory to 2,408 MB after new tests.

## [1.1.0] - 2023-01-20
### Changed
- Power Tuning version bumped to 4.2.1.
- aws-cdk-lib version bumped to 2.61.1.
- cdk-nag version bumped to 2.21.68.

### Fixed
- Removed the access logs from the S3 bucket, which isn't needed in
  this demo application, and was preventing the bucket removal.
- NAG suppressions typos.


## [1.0.0] - 2022-07-03
### Added
- Code to test the parallel deploy.
- Power Tuning to test the Lambda function with different memory
  configurations.
- CDK code to deploy the infrastructure.

[1.1.2]: https://github.com/aws-samples/aws-lambda-parallel-download/tree/v1.1.2
[1.1.1]: https://github.com/aws-samples/aws-lambda-parallel-download/tree/v1.1.1
[1.1.0]: https://github.com/aws-samples/aws-lambda-parallel-download/tree/v1.1.0
[1.0.0]: https://github.com/aws-samples/aws-lambda-parallel-download/tree/v1.0.0