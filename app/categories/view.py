from datetime import datetime

from flask import request, current_app, jsonify
from flask_jwt_extended import current_user, jwt_required

from app import db
from app.models import JournalEntry, Category
from . import category_bp


@category_bp.route("/add", methods=["POST"])
@jwt_required()
def add_category():
    try:
        request_data = request.get_json()
        request_data["user_id"] = current_user.id
        category, response = Category().create(**request_data)
        if not category:
            current_app.logger.error(
                f"[ 400_error ] adding category failed; error: {response}"
            )
            return (
                jsonify({"error": "Request failed. Try again later", "success": False}),
                400,
            )
        current_app.logger.info(f"[ 201_created ] category add successful")
        return (
            jsonify(
                {
                    "msg": "category added successfully",
                    "success": True,
                    "data": category,
                }
            ),
            201,
        )
    except Exception as e:
        current_app.logger.exception(
            f"[ 500_error ] Add category; Exception: {e.args[0]}"
        )
        return (
            jsonify(
                {
                    "error": "Something went wrong. Please try again later",
                    "success": False,
                }
            ),
            500,
        )


@category_bp.route("/update", methods=["PATCH"], endpoint="update_category")
@jwt_required()
def update_category():
    try:
        request_data = request.get_json()
        print(request_data)
        category, response = Category().update_category(current_user.id, **request_data)
        if not category:
            current_app.logger.error(
                f"[ 400_error ] updating category failed; error: {response}"
            )
            return (
                jsonify({"error": "Request failed. Try again later", "success": False}),
                400,
            )
        current_app.logger.info(f"[ 200_ok ] category update successful")
        return (
            jsonify(
                {
                    "msg": "category updateed successfully",
                    "success": True,
                    "data": category,
                }
            ),
            201,
        )
    except Exception as e:
        current_app.logger.exception(
            f"[ 500_error ] Update category; Exception: {e.args[0]}"
        )
        return (
            jsonify(
                {
                    "error": "Something went wrong. Please try again later",
                    "success": False,
                }
            ),
            500,
        )


@category_bp.route("", methods=["GET"], endpoint="get_entries")
@jwt_required()
def get_category():
    try:
        category_id = request.args.get("id")
        if category_id:
            data, response = Category().get_category(current_user.id, category_id)
        else:
            data, response = Category().get_categories(current_user.id)
        if not data:
            current_app.logger.error(
                f"[ 404_error ] fetching categories: {response}"
            )
            return (
                jsonify({"msg": "No categories found", "success": True}),
                200,
            )
        current_app.logger.info(f"[ 200_ok ] category fetch successful")
        return (
            jsonify(
                {
                    "msg": "Request successful",
                    "success": True,
                    "data": data,
                }
            ),
            201,
        )
    except Exception as e:
        current_app.logger.exception(
            f"[ 500_error ] delete category; Exception: {e.args[0]}"
        )
        return (
            jsonify(
                {
                    "error": "Something went wrong. Please try again later",
                    "success": False,
                }
            ),
            500,
        )


@category_bp.route("/delete", methods=["DELETE"], endpoint="delete_category")
@jwt_required()
def delete_category():
    try:
        category_id = request.get_json().get("id")
        category, response = Category().delete_category(current_user.id, category_id)
        if not category:
            current_app.logger.error(
                f"[ 400_error ] updating category failed; error: {response}"
            )
            return (
                jsonify({"error": "Request failed. Try again later", "success": False}),
                400,
            )
        current_app.logger.info(f"[ 200_ok ] category delete successful")
        return (
            jsonify(
                {
                    "msg": "category deleted successfully",
                    "success": True,
                    "data": category,
                }
            ),
            201,
        )
    except Exception as e:
        current_app.logger.exception(
            f"[ 500_error ] delete category; Exception: {e.args[0]}"
        )
        return (
            jsonify(
                {
                    "error": "Something went wrong. Please try again later",
                    "success": False,
                }
            ),
            500,
        )
