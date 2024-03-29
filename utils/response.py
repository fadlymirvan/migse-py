import json
import datetime

from flask import Response


# Use this function to convert datetime.datetime to iso format
def datetime_handler(n):
    if isinstance(n, datetime.datetime):
        return n.isoformat()
    raise TypeError("Unknown type")


# Handler to Create Response from Flask
def ResponseAPI(message, code, data):
    return Response(
        status=code,
        mimetype="application/json",
        response=json.dumps({
            "message": message,
            "status": code,
            "data": data
        }, default=datetime_handler)
    )
