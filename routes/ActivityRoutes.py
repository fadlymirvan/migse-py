from flask import Blueprint

from controllers import ActivityController

# Define the Blueprint Name
activityRoutes = Blueprint('activityRoutes', __name__)

# Register URL Rule with the method
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