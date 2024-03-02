#!/usr/bin/env python3

import boto3, datetime
from botocore.exceptions import ClientError


try: 
	now = datetime.datetime.now()
	current_time = now.strftme("%Y-%m-%d-%H%M")
	training_job_name = 'sagemaker-xgboost-training-job-' + current_time
	smc = boto3.client('sagemaker')
	des = smc.describe_training_job(TrainingJobName=training_job_name)
except ClientError as e:
	print('creating a new job')
	try:
		res = smc.create_training_job(
			TrainingJobName=training_job_name,
			AlgorithmSpecification={ 
				'TrainingImage': '257758044811.dkr.ecr.us-east-2.amazonaws.com/sagemaker-xgboost:1.2-1',
				'TrainingInputMode': 'File'
			},
			HyperParameters={
				'max_depth': '5',
				'eta': '0.2',
				'gamma': '4',
				'min_child_weight': '6',
				'subsample': '0.7',
				'objective': 'binary:logistic',
				'num_round': '1000'
			},
			RoleArn='arn:aws:iam::903207315661:role/service-role/AmazonSageMakerServiceCatalogProductsUseRole',
			InputDataConfig=[
				{
					'ChannelName': 'train',
					'DataSource': {
						'S3DataSource': {
							'S3DataType': 'S3Prefix',
							'S3Uri': 's3://dse-sagemaker-data/test/train.csv',
							'S3DataDistributionType': 'FullyReplicated',
						}
					},
					'ContentType': 'csv',
					'InputMode': 'File'
				},
				{
					'ChannelName': 'validation',
					'DataSource': {
						'S3DataSource': {
							'S3DataType': 'S3Prefix',
							'S3Uri': 's3://dse-sagemaker-data/test/validation.csv',
							'S3DataDistributionType': 'FullyReplicated',
						}
					},
					'ContentType': 'csv',
					'InputMode': 'File'
					
				}
			],
			OutputDataConfig={
				'S3OutputPath': 's3://dse-outbox'
			},
			ResourceConfig={
				'InstanceType': 'ml.m4.xlarge',
				'InstanceCount': 1,
				'VolumeSizeInGB': 5,
			},
			StoppingCondition={
				'MaxRuntimeInSeconds': 86400
			},
		)
	except ClientError as e:
		print(e)
	else:
		print(res)
else:
	print(f'training job "{training_job_name}" already exists.')
#	print(f'updating "{training_job_name}"...')
#	try:
#		res = smc.update_training_job(
#			TrainingJobName=training_job_name
#		)
#	except ClientError as e:
#		print(e)
#	else:
#		print(res)	
