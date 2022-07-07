import datetime
import http.client

from flask import request
from flask.views import MethodView

from middleware import CheckJWT
from models import Attendance
from utils import ResponseAPI


# History Controller to Handle Get History Attendance
class HistoryController(MethodView):
    def get(self):
        isAuth, user_id, auth_token = CheckJWT()  # Check user auth

        if isAuth:  # Validate user Auth
            data = Attendance.get_all_attendance(user_id)  # Get All History CheckIn and CheckOut
            attendances = [obj.to_dict() for obj in data]  # Convert Class List into List of Dictionary

            return ResponseAPI(
                message="Successfully retrieve all Activity",
                code=http.client.OK,
                data={
                    "history": attendances
                }
            )

        else:
            return ResponseAPI(
                message="Unauthorized!",
                code=http.client.UNAUTHORIZED,
                data=None
            )


# To Handle Check In Request
class AttendanceInController(MethodView):
    def post(self):
        isAuth, user_id, auth_token = CheckJWT()  # Check user Auth from JWT
        if isAuth:
            isCheckIn = request.cookies.get("is_checkin")  # Check is_checkin Cookie if already checkin
            if not isCheckIn:
                try:
                    attd = Attendance()
                    attd.user_id = user_id
                    attd.description = "Check In"
                except Exception as err:
                    return ResponseAPI(
                        message=str(err),
                        code=http.client.INTERNAL_SERVER_ERROR,
                        data=None
                    )

                attd.save()  # Save Check In Status into database

                resp = ResponseAPI(
                    message="Check In Successfully",
                    code=http.client.OK,
                    data=None
                )

                # Setup Cookie and set expires date
                resp.set_cookie("is_checkin", "True", expires=datetime.datetime.utcnow() + datetime.timedelta(days=1))
                return resp

            else:
                return ResponseAPI(
                    message="You Have Check-In!",
                    code=http.client.BAD_REQUEST,
                    data=None
                )
        else:
            return ResponseAPI(
                message="Unauthorized!",
                code=http.client.UNAUTHORIZED,
                data=None
            )


# To Handle Check Out Request
class AttendanceOutController(MethodView):
    def post(self):
        isAuth, user_id, auth_token = CheckJWT()  # Check user Auth by JWT
        if isAuth:
            isCheckIn = request.cookies.get("is_checkin")  # Check Cookie if user already Check In
            if isCheckIn:
                try:
                    attd = Attendance()
                    attd.user_id = user_id
                    attd.description = "Check Out"
                except Exception as err:
                    return ResponseAPI(
                        message=str(err),
                        code=http.client.INTERNAL_SERVER_ERROR,
                        data=None
                    )

                attd.save()  # Save Check Out data to Database

                resp = ResponseAPI(
                    message="Check Out Successfully",
                    code=http.client.OK,
                    data=None
                )

                # Remove existing cookie
                resp.delete_cookie("is_checkin")

                return resp

            else:
                return ResponseAPI(
                    message="You Have Not Check-In!",
                    code=http.client.BAD_REQUEST,
                    data=None
                )
        else:
            return ResponseAPI(
                message="Unauthorized!",
                code=http.client.UNAUTHORIZED,
                data=None
            )
