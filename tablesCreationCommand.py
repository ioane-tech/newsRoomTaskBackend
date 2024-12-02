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


users_table_name = "newsRoomUsers"
blogs_table_name = "blogs"
comments_table_name = "comments"


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



# Create blogs table
if blogs_table_name not in existing_tables:
    try:
        blogs_table = dynamodb.create_table(
            TableName=blogs_table_name,
            KeySchema=[
                {"AttributeName": "blogId", "KeyType": "HASH"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "blogId", "AttributeType": "S"},
            ],
            ProvisionedThroughput={
                "ReadCapacityUnits": 5,
                "WriteCapacityUnits": 5,
            },
        )
        print("Blogs Table created successfully.")
    except ClientError as e:
        print(f"Error creating blogs table: {e.response['Error']['Message']}")
else:
    print("Blogs Table already exists.")


# Create Comments table if it doesn't exist
if comments_table_name not in existing_tables:
    try:
        comments_table = dynamodb.create_table(
            TableName=comments_table_name,
            KeySchema=[
                {"AttributeName": "blogId", "KeyType": "HASH"},  
                {"AttributeName": "commentId", "KeyType": "RANGE"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "blogId", "AttributeType": "S"}, 
                {"AttributeName": "commentId", "AttributeType": "S"},
            ],
            ProvisionedThroughput={
                "ReadCapacityUnits": 5,
                "WriteCapacityUnits": 5,
            },
        )
        print("Comments Table created successfully.")
    except ClientError as e:
        print(f"Error creating comments table: {e.response['Error']['Message']}")
else:
    print("Comments Table already exists.")




