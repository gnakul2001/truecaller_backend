import pytz
from rest_framework.views import APIView

from truecaller_backend.serializers import UserSerializer
from truecaller_backend.models import User
from truecaller_backend.helper import (
    get_response,
    check_password,
    encrypt_string,
    generate_random_string,
)
from datetime import datetime, timedelta


class UserRegister(APIView):
    #   Requested Parameters:
    #       - name
    #       - country_code
    #       - phone_number
    #       - password
    #       - email (Optional)
    # This will creates a new user.
    def post(self, request, format=None):
        # Called Serializer.
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # user is valid and now saving it.
            user = serializer.save()
            # return the formatted response.
            return get_response(
                "success", "User created successfully.", UserSerializer(user).data
            )
        else:
            return get_response("error", serializer)


class UserLogin(APIView):
    #   Requested Parameters:
    #       - country_code
    #       - phone_number
    #       - password
    # This will login a user.
    def post(self, request, format=None):
        req_data = request.data
        country_code = req_data.get("country_code", "")
        try:
            phone_number = int(req_data.get("phone_number", 0))
        except Exception:
            return get_response("error", "Invalid Request.")
        password = req_data.get("password", "")

        if country_code == "" or phone_number == 0 or password == "":
            return get_response("error", "Invalid Request.")

        try:
            # Getting user by matching country_code and phone_number.
            user = User.objects.get(
                country_code=country_code,
                phone_number=phone_number,
            )
            # Checking the password provided with the existing one.
            if check_password(password, user.password):
                # Making a new Login Hash and making it expirable after 1 hour.
                user.login_hash = encrypt_string(generate_random_string(50))
                tz = pytz.timezone("UTC")
                user.login_hash_expires_at = datetime.now(tz) + timedelta(hours=1)
                user.save()
                return get_response("success", "User Found", UserSerializer(user).data)
            else:
                return get_response("error", "Password Incorrect")
        except User.DoesNotExist:
            return get_response("error", "User not found")
        except Exception:
            return get_response("error", "Error getting response from server")
