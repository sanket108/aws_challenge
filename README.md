# aws_challenge project

## Problem Statement
Create an API based on AWS services that can create a VPC with multiple subnets and store the results. We need to be able to retrieve the data of created resources from the API. The code should be written in Python. The API should be protected with an authentication layer. Authorization should be open to all authenticated users.

## Overview
- This project provisions an API that:
- Authenticates users using Cognito
- Creates a VPC with subnets
- Stores metadata in DynamoDB
- Allows authenticated users to retrieve VPC data

#### Install cdk
npm i -g aws-cdk

#### Setup Python VirtualEnv
python -m venv venv

#### Change directory

Change your directory to the `cd infrastructure` folder in the terminal while running cdk and pip commands

#### Install python dependencies

pip install -r requirements.txt

## Deploy
```bash
cd infrastructure
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cdk bootstrap -c env=development --profile <prfile-name>
cdk deploy -c env=development --profile <prfile-name> --all
```