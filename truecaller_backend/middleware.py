from truecaller_backend.helper import get_response
from django.urls import resolve
from .helper import get_user_info


class ValidateUserMiddleware:
    # List of view names that are excluded from user validation.
    EXCLUDED_VIEW_NAMES = ["create_user", "login_user", "home"]

    def __init__(self, get_response):
        # Initialize the middleware with the given get_response function.
        self.get_response = get_response

    def __call__(self, request):
        # Get the view name associated with the current request path.
        view_name = resolve(request.path_info).url_name

        # Skip processing for excluded view names, e.g., for login or registration endpoints.
        if view_name in self.EXCLUDED_VIEW_NAMES:
            return self.get_response(request)

        try:
            # Attempt to retrieve user information to validate the request.
            get_user_info(request)
        except Exception as e:
            # If an exception occurs, return an error response.
            return get_response("error", str(e))

        # If validation is successful, proceed with processing the request.
        response = self.get_response(request)
        return response
