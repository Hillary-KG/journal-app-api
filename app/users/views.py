import re
from datetime import datetime, timedelta

from flask import request, current_app, jsonify
from flask_jwt_extended import jwt_required, current_user, decode_token

from app import db
from app.users import users_bp
from app.models import User
from utils.hash_password import hash_password, check_password
from utils.jwt import generate_access_token


@users_bp.route("/register", methods=["POST"])
def register():
    try:
        current_app.logger.info(f"[ start ] user registration ...")
        request_data = request.get_json()
        password_hash = hash_password(request_data.get("password"))

        request_data["password"] = password_hash
        request_data["created_at"] = datetime.now()

        user, response = User().create(**request_data)
        if not user:
            current_app.logger.error(
                f"[ 400_error ] user registration failed; error: {response}"
            )
            return jsonify({"error": response, "success": False}), 400

        current_app.logger.info(
            f"[ 201_created ] user registration successful; user: {request_data.get('username')}"
        )
        return jsonify({"msg": "user registration successful", "success": True}), 201
    except Exception as e:
        current_app.logger.exception(f"[ 500_error ] Login failed. Error: {e.args[0]}")
        return (
            jsonify(
                {"error": "Something went wrong. Try again later", "success": False}
            ),
            500,
        )


@users_bp.route("/login", methods=["POST"])
def login():
    """route to login user"""
    try:
        request_data = request.get_json()
        username, password = request_data.get("username"), request_data.get("password")

        if not (username and password):
            current_app.logger.error(
                f"[ 400_error ] Login failed; Missing username or password"
            )
            return (
                jsonify(
                    {
                        "error": "Bad request. Username and Password Required",
                        "success": False,
                    }
                ),
                400,
            )
        user = User.query.filter_by(username=username).first()
        if not user:
            current_app.logger.error(
                f"[ 404_error ] Login failed; User not found; Username: {username}"
            )
            return jsonify({"error": "User not registered", "success": False}), 404
        if not check_password(password, user.password):
            current_app.logger.error(
                f"[ 401_error ] Login failed; Wrong password; Username: {username}"
            )
            return jsonify({"error": "Wrong password", "success": False}), 401
        access_token, refresh_token, resp = generate_access_token(user.id)
        print(resp)

        user.last_login = datetime.now()
        db.session.add(user)
        db.session.commit()

        current_app.logger.info(f"[ 200_ok ] login successfull; username: {username}")
        return (
            jsonify(
                {
                    "msg": "login successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "success": True,
                }
            ),
            200,
        )
    except Exception as e:
        current_app.logger.exception(f"[ 500_error ] Login failed. Error: {e.args[0]}")
        return (
            jsonify(
                {"error": "Something went wrong. Try again later", "success": False}
            ),
            500,
        )


@users_bp.route("/verify/<token>", methods=["POST"])
def verify(token):
    """route to verify user"""
    try:
        token_payload = decode_token(token)
        user_id = token_payload.get("user_id")
        user = User.query.filter_by(id=user_id).first()

        if not user:
            current_app.logger.error(f"[ 404_error ] verify failed; User not found")
            return jsonify({"error": "User not registered", "success": False}), 404
        current_app.logger.info(
            f"[ 200_ok ] account verification successfull; username: {user.username}"
        )
        return (
            jsonify(
                {
                    "msg": "verification successful",
                    "success": True,
                }
            ),
            200,
        )
    except Exception as e:
        current_app.logger.exception(f"[ 500_error ] verify failed. Error: {e.args[0]}")
        return (
            jsonify(
                {"error": "Something went wrong. Try again later", "success": False}
            ),
            500,
        )


@users_bp.route("/logout", methods=["POST"])
def logout(token):
    """route to logout user"""
    try:
        token_payload = decode_token(token)
        user_id = token_payload.get("user_id")
        user = User.query.filter_by(id=user_id).first()

        if not user:
            current_app.logger.error(f"[ 404_error ] logout failed; User not found")
            return jsonify({"error": "User not registered", "success": False}), 404
        current_app.logger.info(
            f"[ 200_ok ] account verification successfull; username: {user.username}"
        )
        return (
            jsonify(
                {
                    "msg": "verification successful",
                    "success": True,
                }
            ),
            200,
        )
    except Exception as e:
        current_app.logger.exception(f"[ 500_error ] logout failed. Error: {e.args[0]}")
        return (
            jsonify(
                {"error": "Something went wrong. Try again later", "success": False}
            ),
            500,
        )
