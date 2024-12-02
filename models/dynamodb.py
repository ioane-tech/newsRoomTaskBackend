import boto3
from botocore.exceptions import ClientError

from dotenv import load_dotenv
from datetime import datetime
import os


from socketio_instance import socketio



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

userTable_name = "newsRoomUsers"
blogs_table_name = "blogs"
comments_table_name = "comments"

usersTable = dynamodb.Table(userTable_name)
blogsTable = dynamodb.Table(blogs_table_name)
commentsTable =  dynamodb.Table(comments_table_name)


socketio = socketio

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
    

# Add blog to blogs table
def add_blog(blog_id, title, description, image, author):
    try:
        publish_time = datetime.now().isoformat()
        
        blogsTable.put_item(
            Item={
                "blogId": blog_id,
                "title": title,
                "description": description,
                "image": image,
                "publishTime": publish_time,
                "author": author,
            }
        )
        return {"message": "Blog added successfully"}
    except ClientError as e:
        print(e.response["Error"]["Message"])
        return {"error": e.response["Error"]["Message"]}


# get blogs from blogs table
def get_blogs():
    try:
        response = blogsTable.scan()
        return response.get("Items", [])
    except ClientError as e:
        print(e.response["Error"]["Message"])
        return {"error": e.response["Error"]["Message"]}
    
# delete blog
def delete_blog(blog_id):
    try:
        blogsTable.delete_item(
            Key={"blogId": blog_id}
        )
        
        return {"message": "blog deleted successfully"}
    
    except ClientError as e:
        print(e.response["Error"]["Message"])
        return {"error": e.response["Error"]["Message"]}


# Add comment to comments table
def add_comment(blog_id, comment_id, comment):
    try:
        date_of_comment = datetime.now().isoformat()
        
        commentsTable.put_item(
            Item={
                "blogId": blog_id,
                "commentId": comment_id,
                "comment": comment,
                "dateOfComment": date_of_comment,
            }
        )
        return {"message": "Comment added successfully"}
    except ClientError as e:
        print(e.response["Error"]["Message"])
        return {"error": e.response["Error"]["Message"]}


# get comments for blog
def get_comments(blog_id):
    try:
        response = commentsTable.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key("blogId").eq(blog_id)
        )
        return response.get("Items", [])
    except ClientError as e:
        print(e.response["Error"]["Message"])
        return {"error": e.response["Error"]["Message"]}