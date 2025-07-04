from datetime import UTC, datetime, timedelta
from functools import wraps

import jose
from flask import g, jsonify, request
from jose import jwt

SECRET_KEY = "A0P6RS_get_shwifty"

ROLE_SPECIFIC_TIMEOUT = {
    "mechanic": 8,
    "admin": 24,
}


def encode_token(user_id, role):
    payload = {
        "exp": datetime.now(UTC) + timedelta(hours=ROLE_SPECIFIC_TIMEOUT.get(role, 1)),
        "iat": datetime.now(UTC),
        "sub": str(user_id),
        "role": role,
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split()[1]

            if not token:
                return jsonify({"message": "Missing token"}), 401

            try:
                data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                customer_id = data["sub"]
            except jose.exceptions.ExpiredSignatureError:
                return jsonify({"message": "Token expired"}), 400
            except jose.exceptions.JWTError:
                return jsonify({"message": "Invalid Token"}), 400

            return f(customer_id, *args, **kwargs)
        return jsonify({"message": "You must be logged in to access this."}), 400

    return decorated


def role_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]

        if not token:
            return jsonify({"message": "Token is missing or malformed"}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_id = data["sub"]
            role = data["role"]

            if role not in ["mechanic", "admin"]:
                return jsonify({"message": "Forbidden: User not authorized."}), 403

            g.user_id = user_id
            g.user_role = role

        except jose.exceptions.ExpiredSignatureError:
            return jsonify({"message": "Token has expired"}), 401
        except jose.exceptions.JWTError:
            return jsonify({"message": "Invalid token"}), 401

        return f(*args, **kwargs)

    return decorated
