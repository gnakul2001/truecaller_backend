from rest_framework.views import APIView
from truecaller_backend.serializers import SpamContactsSerializer, UserSpammedContactsSerializer
from truecaller_backend.models import SpamContacts, UserSpammedContacts
from truecaller_backend.helper import get_response, generate_random_string, get_user_info


class MarkNumberSpam(APIView):
    #   Requested Parameters:
    #       - country_code
    #       - phone_number
    # This will mark phone number spam.
    def post(self, request, format=None):
        try:
            req_data = request.data
            country_code = req_data.get("country_code", "")
            try:
                phone_number = int(req_data.get("phone_number", 0))
            except Exception:
                return get_response("error", "Invalid Request.")

            if country_code == "" or phone_number == 0:
                return get_response("error", "Invalid Request.")

            # Getting the current logged in user.
            user = get_user_info(request)

            # Checking if user is marking his own mobile number as spam.
            if country_code == user.country_code and phone_number == user.phone_number:
                return get_response("error", "You cannot mark your number as spam.")

            try:
                # Checking if the number already on the spam table.
                spam_contacts = SpamContacts.objects.get(
                    country_code=country_code, phone_number=phone_number
                )
                # Increasing spam count by 1.
                spam_contacts.spam_count += 1
                spam_contacts.save()
                # Taking spam id for making new entry to UserSpammedContacts Table.
                spam_id = spam_contacts.spam_id
            except SpamContacts.DoesNotExist:
                # Number was not on the SpamContacts table. So adding the number in SpamContacts table.
                spam_id = generate_random_string(50)
                serializer = SpamContactsSerializer(
                    data={
                        "spam_id": spam_id,
                        "country_code": country_code,
                        "phone_number": phone_number,
                        "spam_count": 1,
                    }
                )
                if serializer.is_valid():
                    spam_contacts = serializer.save()
                else:
                    return get_response("error", serializer)
            finally:
                # Spam Contact has been updated. Now the time to add record to other table
                # where we are maintaining the user id of the users that spam the number.
                isValid = True
                try:
                    # Checking if the number already on the spam table.
                    user_spam_contacts = UserSpammedContacts.objects.get(
                        user_id=user.user_id, spam_id=spam_id
                    )
                    # Increasing spam count by 1.
                    user_spam_contacts.spam_count += 1
                    user_spam_contacts.save()
                except UserSpammedContacts.DoesNotExist:
                    # User was not on the UserSpammedContacts table.
                    # So adding the number in UserSpammedContacts table.
                    serializer = UserSpammedContactsSerializer(
                        data={
                            "user_id": user.user_id,
                            "spam_id": spam_id,
                            "spam_count": 1,
                        }
                    )
                    if not serializer.is_valid():
                        isValid = False
                        return get_response("error", serializer)
                    serializer.save()
                finally:
                    # return the formatted response.
                    if not isValid:
                        return get_response("error", "Error marking number spam.")
                    return get_response(
                        "success", "Phone number marked spam successfully."
                    )

        except Exception as e:
            return get_response("error", e)
