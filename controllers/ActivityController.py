import http.client

from flask import request
from flask.views import MethodView

from middleware import CheckJWT
from models import Activity
from utils import ResponseAPI


class ActivityController(MethodView):
    def get(self, act_id):
        isAuth, user_id, auth_token = CheckJWT()
        isCheckIn = request.cookies.get("is_checkin")

        if isAuth and isCheckIn:
            if act_id is None:
                dates = Activity.get_date_activity(user_id)
                activities = []

                for date in dates:
                    date = date[0]
                    data = Activity.get_all_activity(user_id, date)
                    activities.append({
                        "date": str(date),
                        "act": [obj.to_dict() for obj in data]
                    })

                return ResponseAPI(
                    message="Successfully retrieve all Activity",
                    code=http.client.OK,
                    data={
                        "result": activities
                    }
                )

            else:
                data = Activity.get_activity_by_id(act_id)
                if not data:
                    return ResponseAPI(
                        message="Activity Not Found",
                        code=http.client.NOT_FOUND,
                        data=None
                    )

                activity = data.to_dict()

                return ResponseAPI(
                    message="Successfully retrieve all Activity",
                    code=http.client.OK,
                    data={
                        "activity": activity
                    }
                )
        else:
            return ResponseAPI(
                message="Unauthorized!",
                code=http.client.UNAUTHORIZED,
                data=None
            )

    def post(self):
        isAuth, user_id, auth_token = CheckJWT()
        isCheckIn = request.cookies.get("is_checkin")

        if isAuth and isCheckIn:
            data = request.get_json()
            if not data.get("title") or not data.get("description"):
                return ResponseAPI(
                    message="Title and Description Field Cannot Be Empty!",
                    code=http.client.BAD_REQUEST,
                    data=None
                )

            try:
                act = Activity(data)
                act.user_id = user_id
            except Exception as err:
                return ResponseAPI(
                    message=str(err),
                    code=http.client.INTERNAL_SERVER_ERROR,
                    data=None
                )

            act.save()

            return ResponseAPI(
                message="Add Activity Successfully",
                code=http.client.CREATED,
                data={
                    "aid": act.id
                }
            )

        else:
            return ResponseAPI(
                message="Unauthorized!",
                code=http.client.UNAUTHORIZED,
                data=None
            )

    def put(self, act_id):
        isAuth, user_id, auth_token = CheckJWT()
        isCheckIn = request.cookies.get("is_checkin")
        if isAuth and isCheckIn:
            if act_id is None:
                return ResponseAPI(
                    message="Parameter ID Cannot Be Empty!",
                    code=http.client.BAD_REQUEST,
                    data=None
                )

            data = request.get_json()
            if not data.get("title") or not data.get("description"):
                return ResponseAPI(
                    message="Title and Description Field Cannot Be Empty!",
                    code=http.client.BAD_REQUEST,
                    data=None
                )

            try:
                activity = Activity.get_activity_by_id(act_id)
                act = Activity(data).to_dict()

            except Exception as err:
                return ResponseAPI(
                    message=str(err),
                    code=http.client.INTERNAL_SERVER_ERROR,
                    data=None
                )

            activity.update(act)

            return ResponseAPI(
                message="Update Activity Successfully",
                code=http.client.OK,
                data={
                    "aid": activity.id
                }
            )

        else:
            return ResponseAPI(
                message="Unauthorized!",
                code=http.client.UNAUTHORIZED,
                data=None
            )

    def delete(self, act_id):
        isAuth, user_id, auth_token = CheckJWT()
        isCheckIn = request.cookies.get("is_checkin")

        if isAuth and isCheckIn:
            if act_id is None:
                return ResponseAPI(
                    message="Parameter ID Cannot Be Empty!",
                    code=http.client.BAD_REQUEST,
                    data=None
                )

            else:
                try:
                    activity = Activity.get_activity_by_id(act_id)

                except Exception as err:
                    return ResponseAPI(
                        message=str(err),
                        code=http.client.INTERNAL_SERVER_ERROR,
                        data=None
                    )

                activity.delete()

                return ResponseAPI(
                    message="Delete Activity Successfully",
                    code=http.client.OK,
                    data=None
                )
        else:
            return ResponseAPI(
                message="Unauthorized!",
                code=http.client.UNAUTHORIZED,
                data=None
            )
