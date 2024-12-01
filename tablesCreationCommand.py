import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
import os

load_dotenv()
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_region = os.getenv("AWS_DEFAULT_REGION")


dynamodb = boto3.resource(
    "dynamodb",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=aws_region
)


users_table_name = "Users"
global_count_table_name = "Global_count"

existing_tables = boto3.client("dynamodb", region_name= aws_region).list_tables()["TableNames"]

# Create Users table if it`s not exists
if users_table_name not in existing_tables:
    try:
        users_table = dynamodb.create_table(
            TableName=users_table_name,
            KeySchema=[
                {"AttributeName": "username", "KeyType": "HASH"} 
            ],
            AttributeDefinitions=[
                {"AttributeName": "username", "AttributeType": "S"}
            ],
            ProvisionedThroughput={
                "ReadCapacityUnits": 5,
                "WriteCapacityUnits": 5,
            },
        )
        print("Users Table created successfully.")
    except ClientError as e:
        print(f"Error creating users table: {e.response['Error']['Message']}")
else:
    print(f"Users Table already exists.")


# Create Global_count table if it`s not exists
if global_count_table_name not in existing_tables:
    try:
        global_count_table = dynamodb.create_table(
            TableName=global_count_table_name,
            KeySchema=[
                {"AttributeName": "username", "KeyType": "HASH"}, 
                {"AttributeName": "date", "KeyType": "RANGE"} 
            ],
            AttributeDefinitions=[
                {"AttributeName": "username", "AttributeType": "S"},
                {"AttributeName": "date", "AttributeType": "S"},
            ],
            ProvisionedThroughput={
                "ReadCapacityUnits": 5,
                "WriteCapacityUnits": 5,
            },
        )
        print(f"Global counts Table created successfully.")
    except ClientError as e:
        print(f"Error creating global counts table: {e.response['Error']['Message']}")
else:
    print(f"Global counts Table already exists.")


