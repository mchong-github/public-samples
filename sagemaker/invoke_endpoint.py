#!/usr/bin/env python3

import boto3

sagemaker_runtime = boto3.client("sagemaker-runtime")
endpoint_name = 'sagemaker-xgboost-2021-12-26-00-37-00-294'
res = sagemaker_runtime.invoke_endpoint(
	EndpointName=endpoint_name,
	Body=bytes('{"features": ["This is great!"]}', 'utf-8')
)

print(res['Body'],read().decode('utf-8'))
