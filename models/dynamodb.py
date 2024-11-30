import boto3
from botocore.exceptions import ClientError
from flask import jsonify
from datetime import datetime


dynamodb = boto3.resource("dynamodb", region_name="us-west-2")

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
        
        return jsonify({"message": "User registered successfully"})
    except ClientError as e:
        print(e.response["Error"]["Message"])
        return jsonify({"error": e.response["Error"]["Message"]}), 500

#get user from users table
def get_user(username):
    try:
        response = usersTable.get_item(Key={"username": username})
        return response.get("Item")
    except ClientError as e:
        print(e.response["Error"]["Message"])
        return jsonify({"error": e.response["Error"]["Message"]}), 500
    


#increment global sing-in counts
def increment_sign_in_count(username, ):
    try:
        today_date = datetime.now().strftime("%Y-%m-%d")

        
        globalCountTable.put_item(
            Item={
                "username": username,
                "date": today_date,
            }
        )
        print(f"Sign-in count for {username} on {today_date} incremented successfully.")
        return jsonify({"message": f"Sign-in count for {username} on {today_date} incremented successfully."})
    except ClientError as e:
        print(e.response["Error"]["Message"])
        return jsonify({"error": e.response["Error"]["Message"]}), 500

#get counts from global counts table
def get_counts(username):
    try:
        if not username:
            response = usersTable.scan()
        else:
            response = usersTable.query(
                KeyConditionExpression="username = :username",
                ExpressionAttributeValues={
                    ":username": username
                }
        )

        #error if user not found
        if not response.get("Items"):
            return jsonify({"message": "No users found with that username"}), 404
        
        return response.get("Items", []), 200
    except ClientError as e:
        print(e.response["Error"]["Message"])
        return jsonify({"error": e.response["Error"]["Message"]}), 500