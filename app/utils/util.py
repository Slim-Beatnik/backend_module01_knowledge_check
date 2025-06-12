from datetime import UTC, datetime, timedelta
from functools import wraps

import jose
from flask import jsonify, request
from jose import jwt

SECRET_KEY = "get_shwifty"


def encode_token(customer_id):
    payload = {
        "exp": datetime.now(UTC) + timedelta(hours=1),
        "iat": datetime.now(UTC),
        "sub": str(customer_id),
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
