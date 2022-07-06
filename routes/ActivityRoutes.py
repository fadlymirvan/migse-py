from flask import Blueprint

from controllers import ActivityController

activityRoutes = Blueprint('activityRoutes', __name__)

activityRoutes.add_url_rule(
    '/', defaults={'act_id': None},
    view_func=ActivityController.as_view('activity_get_url'),
    methods=['GET']
)

activityRoutes.add_url_rule(
    '/',
    view_func=ActivityController.as_view('activity_post_url'),
    methods=['POST']
)

activityRoutes.add_url_rule(
    '/<act_id>',
    view_func=ActivityController.as_view('activity_id_url'),
    methods=['GET', 'PUT', 'DELETE']
)