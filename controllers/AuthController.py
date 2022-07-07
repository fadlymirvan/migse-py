import http.client
import datetime

from flask import request
from flask.views import MethodView

from middleware import CheckJWT
from models import User, Token
from utils import ResponseAPI, Auth


# To Handle Login Request
class LoginController(MethodView):
    def post(self):
        data = request.get_json()  # Get data from Request Body
        if not data.get("email") or not data.get("password"):  # Validate request body
            return ResponseAPI(
                message="Email and Password Field Cannot Be Empty!",
                code=http.client.BAD_REQUEST,
                data=None
            )

        try:
            User(data)  # Set Data into Model
        except Exception as err:
            return ResponseAPI(
                message=str(err),
                code=http.client.INTERNAL_SERVER_ERROR,
                data=None
            )

        # Check if User Exists
        is_user = User.check_email(data.get("email"))
        if not is_user:
            return ResponseAPI(
                message="Invalid Email Address!",
                code=http.client.BAD_REQUEST,
                data=None
            )

        # Validate Password
        if not is_user.check_hash(data.get("password")):
            return ResponseAPI(
                message="Invalid Password!",
                code=http.client.BAD_REQUEST,
                data=None
            )

        # Generate JWT Token
        token = Auth.generate_token(is_user.id)

        resp = ResponseAPI(
            message="Login Successfully",
            code=http.client.OK,
            data={
                "token": token
            }
        )

        # Setup Cookie for token
        resp.set_cookie("token", token, expires=datetime.datetime.utcnow() + datetime.timedelta(days=1))

        return resp


# Handle Logout Request
class LogoutController(MethodView):
    def post(self):
        isAuth, user_id, auth_token = CheckJWT()  # Check user auth or if user already login

        used_token = Token.check_token(auth_token)  # Validate if Token already used
        if not used_token:
            used_token = Token(auth_token)
            # Add Used Token To Database
            used_token.save()

            resp = ResponseAPI(
                message="Logout Successfully",
                code=http.client.OK,
                data=None
            )

            # Remove Cookie
            resp.set_cookie("token", expires=datetime.datetime.utcnow() - datetime.timedelta(days=1))
            resp.delete_cookie("token")

            return resp
        else:
            return ResponseAPI(
                message="Logout Failed!",
                code=http.client.BAD_REQUEST,
                data=None
            )
