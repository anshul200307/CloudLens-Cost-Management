# CloudLens — AWS Cost Management

## What is this?
Automated daily AWS cost reporting
system with anomaly detection.

## AWS Services Used
- AWS Lambda
- AWS Cost Explorer
- Amazon EventBridge
- Amazon SNS
- Amazon S3
- IAM

## Features
- Daily automated reports 9AM IST
- Service wise cost breakdown
- 7 day trend analysis
- Anomaly detection
- S3 report archiving
- Email notifications

## How it works
1. EventBridge triggers Lambda daily
2. Cost Explorer fetches 7 day data
3. Report generated with breakdown
4. S3 pe report save hoti hai
5. Email notification aati hai

## Result


![Email Proof](email_screenshot.png)



## Architecture


![Architecture](diagram.png)



