from datetime import datetime

from flask import request, current_app, jsonify
from flask_jwt_extended import current_user, jwt_required

from app import db
from app.models import JournalEntry, Category
from . import journals_bp


@journals_bp.route("/add", methods=["POST"])
@jwt_required()
def add_journal_entry():
    try:
        request_data = request.get_json()
        request_data["user_id"] = current_user.id
        entry, response = JournalEntry().create(**request_data)
        if not entry:
            current_app.logger.error(
                f"[ 400_error ] adding journal entry failed; error: {response}"
            )
            return (
                jsonify({"error": "Request failed. Try again later", "success": False}),
                400,
            )
        current_app.logger.info(f"[ 201_created ] journal entry add successful")
        return (
            jsonify(
                {
                    "msg": "journal entry added successfully",
                    "success": True,
                    "data": entry,
                }
            ),
            201,
        )
    except Exception as e:
        current_app.logger.exception(
            f"[ 500_error ] Add Journal Entry; Exception: {e.args[0]}"
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


@journals_bp.route("/update", methods=["PATCH"], endpoint="update_entry")
@jwt_required()
def update_journal_entry():
    try:
        request_data = request.get_json()
        # request_data = request.args
        entry, response = JournalEntry().update_journal_entry(current_user.id, **request_data)
        if not entry:
            current_app.logger.error(
                f"[ 400_error ] updating journal entry failed; error: {response}"
            )
            return (
                jsonify({"error": "Request failed. Try again later", "success": False}),
                400,
            )
        current_app.logger.info(f"[ 200_ok ] journal entry update successful")
        return (
            jsonify(
                {
                    "msg": "journal entry updated successfully",
                    "success": True,
                    "data": entry,
                }
            ),
            201,
        )
    except Exception as e:
        current_app.logger.exception(
            f"[ 500_error ] Update Journal Entry; Exception: {e.args[0]}"
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


@journals_bp.route("", methods=["GET"], endpoint="get_entries")
@jwt_required()
def get_journal_entry():
    try:
        entry_id = request.args.get("id")
        if entry_id:
            data, response = JournalEntry().get_journal_entry(current_user.id, entry_id)
        else:
            data, response = JournalEntry().get_journal_entries(current_user.id)
        if not data:
            current_app.logger.error(
                f"[ 404_error ] fetching journal entries ; error: {response}"
            )
            return (
                jsonify({"msg": "Entry not found. Try again later", "success": True}),
                404,
            )
        current_app.logger.info(f"[ 200_ok ] journal entry fetch successful")
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
            f"[ 500_error ] delete Journal Entry; Exception: {e.args[0]}"
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


@journals_bp.route("/delete", methods=["DELETE"], endpoint="delete_entry")
@jwt_required()
def delete_journal_entry():
    try:
        entry_id = request.get_json().get("id")
        entry, response = JournalEntry().delete_journal_entry(current_user.id, entry_id)
        if not entry:
            current_app.logger.error(
                f"[ 400_error ] delete journal entry failed; error: {response}"
            )
            return (
                jsonify({"error": "Request failed. Try again later", "success": False}),
                400,
            )
        current_app.logger.info(f"[ 200_ok ] journal entry delete successful")
        return (
            jsonify(
                {
                    "msg": "journal entry deleted successfully",
                    "success": True,
                    "data": entry,
                }
            ),
            201,
        )
    except Exception as e:
        current_app.logger.exception(
            f"[ 500_error ] delete Journal Entry; Exception: {e.args[0]}"
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
