import datetime
import http.client

from flask import request
from flask.views import MethodView

from middleware import CheckJWT
from models import Attendance
from utils import ResponseAPI


class HistoryController(MethodView):
    def get(self):
        isAuth, user_id, auth_token = CheckJWT()

        if isAuth:
            data = Attendance.get_all_attendance(user_id)
            attendances = [obj.to_dict() for obj in data]

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


class AttendanceInController(MethodView):
    def post(self):
        isAuth, user_id, auth_token = CheckJWT()
        if isAuth:
            isCheckIn = request.cookies.get("is_checkin")
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

                attd.save()

                resp = ResponseAPI(
                    message="Check In Successfully",
                    code=http.client.OK,
                    data=None
                )

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


class AttendanceOutController(MethodView):
    def post(self):
        isAuth, user_id, auth_token = CheckJWT()
        if isAuth:
            isCheckIn = request.cookies.get("is_checkin")
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

                attd.save()

                resp = ResponseAPI(
                    message="Check Out Successfully",
                    code=http.client.OK,
                    data=None
                )

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
