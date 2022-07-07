import http.client

from flask import request
from flask.views import MethodView

from middleware import CheckJWT
from models import Activity
from utils import ResponseAPI


# Activity Controller to Handle Activity Request
class ActivityController(MethodView):
    # To Handle GET Request
    def get(self, act_id):
        isAuth, user_id, auth_token = CheckJWT()  # Checking user Auth by its JWT
        isCheckIn = request.cookies.get("is_checkin")  # Check is_checkin Cookie

        if isAuth and isCheckIn:
            if act_id is None:
                # Get Distinct Date from Activity. The Activity will be group from created_at
                dates = Activity.get_date_activity(user_id)
                activities = []

                for date in dates:
                    date = date[0]
                    data = Activity.get_all_activity(user_id, date)
                    activities.append({
                        "date": str(date),
                        "act": [obj.to_dict() for obj in data]
                    })

                # Return All Activity Grouped By Date
                return ResponseAPI(
                    message="Successfully retrieve all Activity",
                    code=http.client.OK,
                    data={
                        "result": activities
                    }
                )

            else:
                # Get Activity by ID
                data = Activity.get_activity_by_id(act_id)
                if not data:
                    return ResponseAPI(
                        message="Activity Not Found",
                        code=http.client.NOT_FOUND,
                        data=None
                    )

                # Convert Data class to disctionary
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

    # To Handle POST Request
    def post(self):
        isAuth, user_id, auth_token = CheckJWT()  # Checking user auth by JWT
        isCheckIn = request.cookies.get("is_checkin")  # Check is_checkin cookie if user checkin already

        if isAuth and isCheckIn:
            data = request.get_json()  # Get data From Body
            # Validate Request Body
            if not data.get("title") or not data.get("description"):
                return ResponseAPI(
                    message="Title and Description Field Cannot Be Empty!",
                    code=http.client.BAD_REQUEST,
                    data=None
                )

            try:
                act = Activity(data)  # Fit the Request to Model
                act.user_id = user_id
            except Exception as err:
                return ResponseAPI(
                    message=str(err),
                    code=http.client.INTERNAL_SERVER_ERROR,
                    data=None
                )

            act.save()  # Save data to Database

            return ResponseAPI(
                message="Add Activity Successfully",
                code=http.client.CREATED,
                data={
                    "aid": act.to_dict()
                }
            )

        else:
            return ResponseAPI(
                message="Unauthorized!",
                code=http.client.UNAUTHORIZED,
                data=None
            )

    # To Handle PUT Request
    def put(self, act_id):
        isAuth, user_id, auth_token = CheckJWT()  # Checking user auth by JWT
        isCheckIn = request.cookies.get("is_checkin")  # Check is_checkin Cookie is user already CheckIn
        if isAuth and isCheckIn:  # Validate user auth and checkin
            if act_id is None:  # validate if Param is not Null
                return ResponseAPI(
                    message="Parameter ID Cannot Be Empty!",
                    code=http.client.BAD_REQUEST,
                    data=None
                )

            data = request.get_json()  # Get data from Request Body
            # Validate Request Body
            if not data.get("title") or not data.get("description"):
                return ResponseAPI(
                    message="Title and Description Field Cannot Be Empty!",
                    code=http.client.BAD_REQUEST,
                    data=None
                )

            try:
                activity = Activity.get_activity_by_id(act_id)  # Find the old Data from Database by ID
                act = Activity(data)  # Fit the New Value to Model
                act.user_id = user_id

            except Exception as err:
                return ResponseAPI(
                    message=str(err),
                    code=http.client.INTERNAL_SERVER_ERROR,
                    data=None
                )

            activity.update(act)  # Update data and save it to database

            return ResponseAPI(
                message="Update Activity Successfully",
                code=http.client.OK,
                data={
                    "aid": activity.to_dict()
                }
            )

        else:
            return ResponseAPI(
                message="Unauthorized!",
                code=http.client.UNAUTHORIZED,
                data=None
            )

    # To Handle DELETE Request
    def delete(self, act_id):
        isAuth, user_id, auth_token = CheckJWT()  # Checking user auth by JWT
        isCheckIn = request.cookies.get("is_checkin")  # Check is_checkin Cookie if user Check In already

        if isAuth and isCheckIn:  # Validate user auth and cookie
            if act_id is None:  # Check if param is not Null
                return ResponseAPI(
                    message="Parameter ID Cannot Be Empty!",
                    code=http.client.BAD_REQUEST,
                    data=None
                )

            else:
                try:
                    activity = Activity.get_activity_by_id(act_id)  # Get the data from database

                except Exception as err:
                    return ResponseAPI(
                        message=str(err),
                        code=http.client.INTERNAL_SERVER_ERROR,
                        data=None
                    )

                activity.delete()  # Delete data

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
