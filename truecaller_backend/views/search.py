from itertools import chain
from rest_framework.views import APIView
from truecaller_backend.models import Contacts, SpamContacts, User
from truecaller_backend.helper import get_response, get_user_info
from django.db.models import Q, Subquery, OuterRef, IntegerField
from django.db.models.functions import Coalesce


class SearchByName(APIView):
    # Requested Parameters:
    #       - name
    #       - page_no
    #       - max_result
    # This will search for the contacts by name
    def post(self, request, format=None):
        req_data = request.data

        name = req_data.get("name", "")
        try:
            page_no = int(req_data.get("page_no", 1))
            max_result = int(req_data.get("max_result", 10))
        except Exception:
            return get_response("error", "Invalid Request.")

        if name == "" or page_no <= 0 or max_result <= 0:
            return get_response("error", "Invalid Request.")

        # Subquery to get spam count for each contact
        spam_count_subquery = SpamContacts.objects.filter(
            country_code=OuterRef("country_code"), phone_number=OuterRef("phone_number")
        ).values("spam_count")[:1]

        # Query to get contacts that start with the provided name
        start_with_name = (
            Contacts.objects.filter(name__istartswith=name)
            .annotate(
                spam_count=Coalesce(
                    Subquery(spam_count_subquery), 0, output_field=IntegerField()
                )
            )
            .values("contact_id", "name", "country_code", "phone_number", "spam_count")
        )

        # Query to get contacts that contain the provided name, excluding those that start with the name
        contain_name = (
            Contacts.objects.filter(
                ~Q(id__in=start_with_name.values_list("id", flat=True)),
                name__icontains=name,
            )
            .annotate(
                spam_count=Coalesce(
                    Subquery(spam_count_subquery), 0, output_field=IntegerField()
                )
            )
            .values("contact_id", "name", "country_code", "phone_number", "spam_count")
        )

        # Get the pagination results for start_with_name and contain_name
        page_result = get_page_results(
            page_no, max_result, start_with_name.count(), contain_name.count()
        )

        start_with_name_counts = page_result["start_with_name"]
        contain_counts = page_result["contain_name"]

        # Fetch the results for start_with_name and contain_name based on pagination
        start_with_results = start_with_name[
            start_with_name_counts[0]: start_with_name_counts[1]
        ]
        contain_results = contain_name[contain_counts[0]: contain_counts[1]]

        # Combine the results
        final_results = list(chain(start_with_results, contain_results))

        return get_response("success", "Results", final_results)


def get_page_results(page_no, max_result, start_with_name_count, contain_name_count):
    # Calculate the number of full pages for start_with_name
    full_pages_start_with_name = start_with_name_count // max_result

    # Handling the pages that only include start_with_name
    if page_no <= full_pages_start_with_name:
        start_with_name_start = (page_no - 1) * max_result
        start_with_name_end = start_with_name_start + max_result
        return {
            "start_with_name": (start_with_name_start, start_with_name_end),
            "contain_name": (0, 0),
        }

    # Handling the page that includes the remaining part of start_with_name and starts with contain_name
    if page_no == full_pages_start_with_name + 1:
        start_with_name_start = full_pages_start_with_name * max_result
        start_with_name_end = start_with_name_count
        contain_name_start = 0
        contain_name_end = max_result - (start_with_name_count % max_result)
        return {
            "start_with_name": (start_with_name_start, start_with_name_end),
            "contain_name": (contain_name_start, contain_name_end),
        }

    # Handling the pages that only include contain_name
    contain_name_start = (
        (page_no - full_pages_start_with_name - 2) * max_result
        + max_result
        - (start_with_name_count % max_result)
    )
    contain_name_end = contain_name_start + max_result

    # Ensure the start and end are within bounds of contain_name_count
    contain_name_start = (
        0 if contain_name_start > contain_name_count else contain_name_start
    )
    contain_name_end = (
        contain_name_end
        if contain_name_end < contain_name_count
        else (0 if contain_name_start > contain_name_count else contain_name_count)
    )

    return {
        "start_with_name": (0, 0),
        "contain_name": (contain_name_start, contain_name_end),
    }


class SearchByPhoneNumber(APIView):
    # Requested Parameters:
    #   - country_code
    #   - phone_number
    #   - page_no
    #   - max_result
    # This will search for the contacts by country_code and phone_number
    def post(self, request, format=None):
        req_data = request.data

        country_code = req_data.get("country_code", "")
        try:
            phone_number = int(req_data.get("phone_number", 0))
            page_no = int(req_data.get("page_no", 1))
            max_result = int(req_data.get("max_result", 10))
        except Exception:
            return get_response("error", "Invalid Request.")

        # Validate the parameters
        if phone_number == 0 or country_code == "" or page_no <= 0 or max_result <= 0:
            return get_response("error", "Invalid Request.")

        # Check if the user exists in the User table
        user = (
            User.objects.filter(country_code=country_code, phone_number=phone_number)
            .values("user_id", "name", "country_code", "phone_number")
            .first()
        )

        # If user exists, get spam count and return the user details
        if user is not None:
            spam_count = 0
            try:
                # Checking if the number is already on the spam table
                user_spam_contacts = SpamContacts.objects.get(
                    country_code=country_code, phone_number=phone_number
                )
                spam_count = user_spam_contacts.spam_count
            finally:
                # Return the formatted response
                user["spam_count"] = spam_count
                return get_response("success", "Results", [user])

        # Create a subquery to get spam count
        spam_count_subquery = SpamContacts.objects.filter(
            country_code=OuterRef("country_code"), phone_number=OuterRef("phone_number")
        ).values("spam_count")[:1]

        # Query the Contacts table to get the list of contacts with the given phone number
        phone_number_list = (
            Contacts.objects.filter(
                country_code=country_code, phone_number=phone_number
            )
            .annotate(
                spam_count=Coalesce(
                    Subquery(spam_count_subquery), 0, output_field=IntegerField()
                )
            )
            .values("contact_id", "name", "country_code", "phone_number", "spam_count")
        )

        # Paginate the results
        offset = (page_no - 1) * max_result
        limit = offset + max_result

        phone_number_list_results = list(phone_number_list[offset:limit])

        return get_response("success", "Results", phone_number_list_results)


class GetDetailByContactId(APIView):
    # Requested Parameters:
    #   - contact_id
    # This will search for the contacts by contact_id
    def post(self, request, format=None):
        req_data = request.data

        contact_id = req_data.get("contact_id", "")

        # Validate the contact_id parameter
        if contact_id == "":
            return get_response("error", "Invalid Request.")

        # Query the Contacts table to find the contact by contact_id
        contacts = (
            Contacts.objects.filter(contact_id=contact_id)
            .values("contact_id", "name", "country_code", "phone_number")
            .first()
        )
        if contacts is None:
            return get_response("error", "Contact Not Found")

        spam_count = 0
        try:
            # Check if the number is already on the spam table
            user_spam_contacts = SpamContacts.objects.get(
                country_code=contacts["country_code"],
                phone_number=contacts["phone_number"],
            )
            spam_count = user_spam_contacts.spam_count
        finally:
            contacts["spam_count"] = spam_count
            email = None
            try:
                cUser = get_user_info(request)
                user = User.objects.get(
                    country_code=contacts["country_code"],
                    phone_number=contacts["phone_number"],
                )
                Contacts.objects.get(
                    user_id_imported_contacts=user.user_id,
                    country_code=cUser.country_code,
                    phone_number=cUser.phone_number,
                )
                email = user.email
            except (Contacts.DoesNotExist, User.DoesNotExist):
                pass
            except Exception as e:
                return get_response("error", str(e))

            # Remove email from the response if the contact does not exist
            if email is not None:
                contacts["email"] = email
            # Return the formatted response with spam count
            return get_response("success", "Contact Found", contacts)


class GetDetailByUserId(APIView):
    # Requested Parameters:
    #   - user_id
    # This will search for the contacts by user_id
    def post(self, request, format=None):
        req_data = request.data

        user_id = req_data.get("user_id", "")

        # Validate the user_id parameter
        if user_id == "":
            return get_response("error", "Invalid Request.")

        # Query the User table to find the contact by user_id
        user = (
            User.objects.filter(user_id=user_id)
            .values("user_id", "name", "country_code", "phone_number", "email")
            .first()
        )

        if user is None:
            return get_response("error", "Contact Not Found")

        spam_count = 0
        try:
            user_spam_contacts = SpamContacts.objects.get(
                country_code=user["country_code"], phone_number=user["phone_number"]
            )
            spam_count = user_spam_contacts.spam_count
        finally:
            user["spam_count"] = spam_count
            isContactExists = False
            try:
                cUser = get_user_info(request)
                Contacts.objects.get(
                    user_id_imported_contacts=user_id,
                    country_code=cUser.country_code,
                    phone_number=cUser.phone_number,
                )
                isContactExists = True
            except Contacts.DoesNotExist:
                pass
            except Exception as e:
                return get_response("error", str(e))

            # Remove email from the response if the contact does not exist
            if not isContactExists:
                del user["email"]
            # Check if the number is already on the spam table
            return get_response("success", "Contact Found", user)
