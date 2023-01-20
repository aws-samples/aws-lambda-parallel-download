# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [1.0.0] - 2022-07-03
### Added
- Code to test the parallel deploy.
- Power Tuning to test the Lambda function with different memory
  configurations.
- CDK code to deploy the infrastructure.

## [1.1.0] - 2023-01-20
### Changed
- Power Tuning version bumped to 4.2.1.
- aws-cdk-lib version bumped to 2.61.1.
- cdk-nag version bumped to 2.21.68.

### Fixed
- Removed the access logs from the S3 bucket, which isn't needed in
  this demo application, and was preventing the bucket removal.
- NAG suppressions typos.


[1.0.0]: https://gitlab.aws.dev/eduborto/apg-lambda-parallel-download/-/tree/v1.0.0
[1.1.0]: https://gitlab.aws.dev/eduborto/apg-lambda-parallel-download/-/tree/v1.0.0