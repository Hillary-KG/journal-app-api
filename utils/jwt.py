"""this module holds jwt functioalities for auth"""

from datetime import timedelta
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
)


def generate_access_token(user_id):
    """
    function to generate access token
    params: <dict> user id payload
    return <tuple> auth_token, refresh_token
    """

    try:
        identity = {"_id": user_id}

        jwt, refresh_token = create_access_token(
            identity=identity, expires_delta=timedelta(hours=24)
        ), create_refresh_token(identity=identity, expires_delta=timedelta(hours=72))

        return str(jwt), str(refresh_token), "success"
    except Exception as e:
        # log exception
        return None, None, f"Exception occured: {e}"


def refresh_token():
    identity = get_jwt_identity()
    new_access_token = create_access_token(identity=identity)
    return new_access_token


def generate_token(payload, ttl=300):
    """generate a generic jwt token"""
    try:
        token = create_access_token(
            identity=payload, expires_delta=timedelta(seconds=ttl)
        )
        return token, "success"
    except Exception as e:
        return None, f"500_error: {e.args[0]}"
