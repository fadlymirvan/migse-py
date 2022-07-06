from flask import Blueprint

from controllers import AttendanceInController, AttendanceOutController, HistoryController

attendanceRoutes = Blueprint('attendanceRoutes', __name__)

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
