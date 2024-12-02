from flask import Blueprint, request, jsonify
from models.dynamodb import add_blog, get_blogs, add_comment, get_comments, delete_blog
import uuid

blogs_bp = Blueprint("blogs", __name__)


# add blog
@blogs_bp.route("/add-blog", methods=["POST"])
def add_blog_route():
    data = request.get_json()
    title = data.get("title")
    description = data.get("description")
    image = data.get("image")
    author = data.get("author")

    if not title or not description or not author:
        return jsonify({"message": "Title, description, and author are required"}), 400

    blog_id = str(uuid.uuid4())
    response = add_blog(blog_id, title, description, image, author)
    
    if 'error' in response:
        return jsonify({"message": response["error"]}), 500
    
    return jsonify({"message": response["message"], "blogId": blog_id}), 201

# fetch blogs
@blogs_bp.route("/get-blogs", methods=["GET"])
def get_blogs_route():
    response = get_blogs()
    
    if "error" in response:
        return jsonify({"message": response["error"]}), 500
    
    return jsonify({"blogs": response}), 200

# delete blog
@blogs_bp.route("/delete-blog/<blog_id>", methods=["DELETE"])
def delete_blog_route(blog_id):
    response = delete_blog(blog_id)
    
    if "error" in response:
        return jsonify({"message": response["error"]}), 500
    
    return jsonify({"message": response["message"]}), 200

# add comment
@blogs_bp.route("/add-comment", methods=["POST"])
def add_comment_route():
    data = request.get_json()
    blog_id = data.get("blogId")
    comment = data.get("comment")

    if not blog_id or not comment:
        return jsonify({"message": "Blog ID and comment are required"}), 400

    comment_id = str(uuid.uuid4())  # Generate a unique ID for the comment
    response = add_comment(blog_id, comment_id, comment)
    
    if 'error' in response:
        return jsonify({"message": response["error"]}), 500

    return jsonify({"message": response["message"], "commentId": comment_id}), 201

# fetch comments
@blogs_bp.route("/get-comments/<blog_id>", methods=["GET"])
def get_comments_route(blog_id):
    response = get_comments(blog_id)
    
    if "error" in response:
        return jsonify({"message": response["error"]}), 500

    return jsonify({"comments": response}), 200
