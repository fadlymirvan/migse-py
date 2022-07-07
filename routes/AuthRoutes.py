from flask import Blueprint

from controllers import LoginController, LogoutController

# Define the Blueprint Name
authRoutes = Blueprint('authRoutes', __name__)

# Register URL Rule with the method
authRoutes.add_url_rule(
    "/login",
    view_func=LoginController.as_view('login_url'),
    methods=['POST']
)

authRoutes.add_url_rule(
    "/logout",
    view_func=LogoutController.as_view('logout_url'),
    methods=['POST']
)
