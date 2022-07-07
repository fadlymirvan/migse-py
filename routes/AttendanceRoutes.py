from flask import Blueprint

from controllers import AttendanceInController, AttendanceOutController, HistoryController

# Define the Blueprint Name
attendanceRoutes = Blueprint('attendanceRoutes', __name__)

# Register URL Rule with the method
attendanceRoutes.add_url_rule(
    '/checkin',
    view_func=AttendanceInController.as_view('checkin_url'),
    methods=['POST']
)

attendanceRoutes.add_url_rule(
    '/checkout',
    view_func=AttendanceOutController.as_view('checkout_url'),
    methods=['POST']
)

attendanceRoutes.add_url_rule(
    '/history',
    view_func=HistoryController.as_view('history_url'),
    methods=['GET']
)
