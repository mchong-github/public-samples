#!/usr/bin/env python3

import boto3, io, datetime
import pandas as pd
from botocore.exceptions import ClientError

bucket = 'dse-sagemaker-data'
test_csv_file = 'test/train.csv'

s3c = boto3.client('s3')

try:
	res = s3c.get_object(Bucket=bucket, Key=test_csv_file)
except ClientError as e:
	print(e)
else:
	df = pd.read_csv(io.BytesIO(res['Body'].read()))
	print(df.head())
	now = datetime.datetime.now()
	print(now.strftime("%Y-%m-%d-%H%M"))
