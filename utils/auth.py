import datetime
import os

import jwt


class Auth:
    # Function to generate token/JWT
    @staticmethod
    def generate_token(user_id):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),  # Expired Date
                'iat': datetime.datetime.utcnow(),  # Create Date
                'uid': user_id  # User ID
            }

            return jwt.encode(
                payload,
                os.getenv("JWT_SECRET_KEY"),
                'HS256'
            )

        except Exception as err:
            return err

    # Function to decode token/JWT to get Data such as user_id, expired_date, or even Validate
    @staticmethod
    def decode_token(token):
        decode_token = {"data": {}, "error": {}}

        try:
            payload = jwt.decode(token, os.getenv('JWT_SECRET_KEY'), 'HS256')
            decode_token['data'] = {'user_id': payload['uid']}
            return decode_token

        except jwt.ExpiredSignatureError:
            decode_token['error'] = {"message": "Token Expired, Please Login Again."}
            return decode_token

        except jwt.InvalidTokenError:
            decode_token['error'] = {"message": "Invalid Token, Please Try Again."}
            return decode_token
