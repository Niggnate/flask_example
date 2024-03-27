from authentication_token_verifier import AuthenticationTokenVerifier
from functools import wraps
from flask import Flask, request, make_response, jsonify

app = Flask(__name__)
app.config['SECRET_TOKEN'] = "mysecret"

authentication_token_verifier = AuthenticationTokenVerifier("token.txt")


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token, error = authentication_token_verifier.read_data()
        if error:
            return make_response(jsonify({"message": "Something went wrong."}), 501)

        authorization = request.headers.get('Authorization')
        if authorization is None:  # return error if no token provided
            return make_response(jsonify({"message": "A valid token is missing!"}), 401)

        bearer_token = authorization.split()[1]

        if bearer_token != token:
            return make_response(jsonify({"message": "Invalid token!"}), 401)

        # Return the user information attached to the token
        return f(bearer_token, *args, **kwargs)

    return decorator


@app.route("/api/v1/protected")
@token_required
def protected(token):
    return make_response({"message": "private place", "data": token})


@app.route("/api/v1/unprotected", methods=['POST'])
def unprotected():
    token = authentication_token_verifier.create_file()
    if token == "exists":
        return make_response(jsonify({"message": "Already have a token!"}), 405)
    elif token == "error":
        return make_response(jsonify({"message": "Something went wrong!"}), 405)
    return make_response({"message": f"Your token is ready!", "token" : token})


if __name__ == "__main__":
    app.run(debug=True)
