import random
import string
from django.http import JsonResponse
import bcrypt
from truecaller_backend.models import User
from datetime import datetime
import pytz


# Generate Random String. Default Length = 10
def generate_random_string(length=10):
    letters_and_digits = string.ascii_letters + string.digits
    return "".join(random.choice(letters_and_digits) for i in range(length))


# Generate Random Number. Default Length = 10
def generate_random_number(length=10):
    digits = string.digits
    return "".join(random.choice(digits) for i in range(length))


# Encrypt the Password using BCrypt.
def encrypt_string(password):
    # Returing the encrypted hash.
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode()


# Checking the plain text password and the encrypted hash.
def check_password(plain_password, hashed_password):
    # Returing whether the plain password is the acctual one or not.
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def remove_none_values(data):
    # Function to remove keys with None values from a dictionary
    def clean_dict(d):
        return {k: v for k, v in d.items() if v is not None}

    if isinstance(data, dict):
        return clean_dict(data)
    elif isinstance(data, list):
        return [clean_dict(d) if isinstance(d, dict) else d for d in data]
    else:
        raise TypeError("Data must be a dictionary or a list of dictionaries.")


def get_response(status, message, data=None):
    if status not in ("success", "error"):
        status = "error"

    # Checking if message is not a string then fetch message from serializers.
    message = (
        message
        if isinstance(message, str)
        else f"{list(message.errors.keys())[0]}: {list(message.errors.values())[0][0]}"
    )

    data = remove_none_values(data) if data is not None else None

    return JsonResponse(
        {
            "status": status,
            "message": message,
            "data": data,
        },
        status=200 if status == "success" else 400,
        safe=False,
    )


def get_user_info(request):
    try:
        user_id = request.headers.get("user-id")  # getting user-id from the header.

        # getting Authorization bearer header.
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            login_hash = auth_header[
                7:
            ]  # getting login_hash from the Authorization bearer header.
        else:
            raise Exception("Missing or invalid Authorization header")

        user = User.objects.get(user_id=user_id, login_hash=login_hash)
        tz = pytz.timezone("UTC")
        if user.login_hash_expires_at and user.login_hash_expires_at.astimezone(
            tz
        ) <= datetime.now(tz):
            raise Exception("Login time expired")

        if user.user_id == "":
            raise Exception("User error")
        return user
    except User.DoesNotExist:
        raise Exception("User not found")
    except Exception as e:
        raise Exception(e)
