from authentication_token_verifier import AuthenticationTokenVerifier
from functools import wraps
from flask import Flask, request, make_response, jsonify

app = Flask(__name__)
app.config['SECRET_TOKEN'] = "mysecret"

_data = AuthenticationTokenVerifier("token.txt")
current_token = _data.read_data()[1]

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        _token = request.headers.get('Authorization').split()[1]
        print(_token)

        if not _token and _token is None:  # throw error if no token provided
            return make_response(jsonify({"message": "A valid token is missing!"}), 401)

        if _token != f"{current_token}":
            return make_response(jsonify({"message": "Invalid token!"}), 401)

        token = _token

        # Return the user information attached to the token
        return f(*args, **kwargs)

    return decorator



@app.route("/api/v1/protected")
@token_required
def protected():
    return make_response({"message": "private place"})


@app.route("/api/v1/unprotected")
def unprotected():
    return make_response({"message": "public place"})


if __name__ == "__main__":
    app.run(debug=True)
