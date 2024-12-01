import boto3
from botocore.exceptions import NoCredentialsError
from botocore.exceptions import ClientError

from dotenv import load_dotenv
from datetime import datetime
import os
from websocket.handler import check_global_counts_length



load_dotenv()
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_region = os.getenv("AWS_DEFAULT_REGION")

# create connection to data base
dynamodb = boto3.resource(
    "dynamodb",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=aws_region
)

userTable_name = "Users"
globalCountTable_name = "Global_count"

usersTable = dynamodb.Table(userTable_name)
globalCountTable = dynamodb.Table(globalCountTable_name)


# create user in users table
def create_user(username, password):
    try:
        usersTable.put_item(
            Item={
                "username": username,
                "password": password,
            }
        ) 
        return {"message": "User registered successfully"}
    except ClientError as e:
        print(e.response["Error"]["Message"])
        return {"error": e.response["Error"]["Message"]}

#get user from users table
def get_user(username):
    try:
        response = usersTable.get_item(Key={"username": username})
        return response.get("Item")
    except ClientError as e:
        print(e.response["Error"]["Message"])
        return {"error": e.response["Error"]["Message"]}
    
#get counts from global counts table
def get_counts(username):
    try:
        if not username:
            response = globalCountTable.scan()
        else:
            response = globalCountTable.query(
                KeyConditionExpression="username = :username",
                ExpressionAttributeValues={
                    ":username": username
                }
        )

        #error if user not found
        if not response.get("Items"):
            return {"message": "No users found with that username"}
        
        return response.get("Items", [])
    except ClientError as e:
        print(e.response["Error"]["Message"])
        return {"error": e.response["Error"]["Message"]}

#increment global sing-in counts
def increment_sign_in_count(username, ):
    try:
        today_date = datetime.utcnow().isoformat()

        
        globalCountTable.put_item(
            Item={
                "username": username,
                "date": today_date,
            }
        )
        print(f"Sign-in count for {username} on {today_date} incremented successfully.")
        
        check_global_counts_length()
        
        return {"message": f"Sign-in count for {username} on {today_date} incremented successfully."}
    except ClientError as e:
        print(e.response["Error"]["Message"])
        return {"error": e.response["Error"]["Message"]}

    
    
def get_global_counts_length():
    try:
        response = globalCountTable.scan()
        return len(response['Items'])
    except NoCredentialsError:
        print("Credentials not available")
        return 0
    except Exception as e:
        print(f"Error checking DynamoDB table: {e}")
        return 0