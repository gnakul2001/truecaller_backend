from django.urls import reverse
from rest_framework.test import APITestCase
from truecaller_backend.helper import encrypt_string, generate_random_string
from truecaller_backend.models import User, SpamContacts, UserSpammedContacts


class UserRegistrationTests(APITestCase):
    def setUp(self):
        # Setting up common data for user login tests
        self.count = 4

    def test_successful_user_registration(self):
        # Test case for successful user registration
        # Defined the url and the data to be sent in the request
        url = reverse("create_user")
        data = {
            "name": "Nakul Gupta",
            "country_code": "+91",
            "phone_number": "8802631741",
            "password": "Nakul@12345",
        }
        # Make a POST request to the url with the given data
        response = self.client.post(url, data, format="json")
        # Check that the response status code is 200 OK
        self.assertEqual(response.status_code, 200)
        # Check that the number of User objects in the database is self.count
        self.assertEqual(User.objects.count(), self.count)
        self.count += 1
        # Check that the data attribute is not empty.
        self.assertTrue(len(response.json()["data"]) > 0)
        # Check that the user_id attribute is present in the response data.
        self.assertTrue("user_id" in response.json()["data"])
        # Check that the name attribute is present in the response data.
        self.assertTrue("name" in response.json()["data"])
        # Check that the country_code attribute is present in the response data.
        self.assertTrue("country_code" in response.json()["data"])
        # Check that the phone_number attribute is present in the response data.
        self.assertTrue("phone_number" in response.json()["data"])
        # Check that the email attribute is not present in the response data.
        self.assertTrue("email" not in response.json()["data"])

    def test_successful_user_registration_with_email(self):
        # Test case for successful user registration with email too.
        # Defined the url and the data to be sent in the request
        url = reverse("create_user")
        data = {
            "name": "Nakul Gupta",
            "country_code": "+91",
            "phone_number": "8802631742",
            "password": "Nakul@12345",
            "email": "nakulgupta1042@gmail.com",
        }
        # Make a POST request to the url with the given data
        response = self.client.post(url, data, format="json")
        # Check that the response status code is 200 OK
        self.assertEqual(response.status_code, 200)
        # Check that the number of User objects in the database is self.count
        self.assertEqual(User.objects.count(), self.count)
        self.count += 1
        # Check that the data attribute is not empty.
        self.assertTrue(len(response.json()["data"]) > 0)
        # Check that the user_id attribute is present in the response data.
        self.assertTrue("user_id" in response.json()["data"])
        # Check that the name attribute is present in the response data.
        self.assertTrue("name" in response.json()["data"])
        # Check that the country_code attribute is present in the response data.
        self.assertTrue("country_code" in response.json()["data"])
        # Check that the phone_number attribute is present in the response data.
        self.assertTrue("phone_number" in response.json()["data"])
        # Check that the email attribute is present in the response data.
        self.assertTrue("email" in response.json()["data"])

    def test_user_registration_with_missing_fields(self):
        # Test case for user registration with missing required fields
        # Defined the url and the data with missing fields
        url = reverse("login_user")
        data = {"name": "Nakul Gupta", "country_code": "+91"}
        # Make a POST request to the url with the given data
        response = self.client.post(url, data, format="json")
        # Check that the response status code is 400 BAD REQUEST.
        self.assertEqual(response.status_code, 400)


class UserLoginTests(APITestCase):
    def setUp(self):
        # Setting up common data for user login tests
        self.country_code = "+91"
        self.phone_number = "8802631741"
        self.password = "Nakul@12345"
        self.phone_number_2 = (
            "9524765741"  # Second phone number for testing non-existent users
        )
        self.wrongpassword = (
            "Nakul@67890"  # Incorrect password for testing wrong credentials
        )
        self.user = User.objects.create(
            user_id=generate_random_string(50),
            name="Nakul Gupta",
            country_code=self.country_code,
            phone_number=self.phone_number,
            password=encrypt_string(self.password),
        )

    def test_successful_user_login(self):
        # Test case for successful user login
        url = reverse("login_user")
        data = {
            "country_code": self.country_code,
            "phone_number": self.phone_number,
            "password": self.password,
        }
        # Make a POST request to the url with the given data
        response = self.client.post(url, data, format="json")
        # Check that the response status code is 200 OK
        self.assertEqual(response.status_code, 200)
        # Check that the data attribute is not empty.
        self.assertTrue(len(response.json()["data"]) > 0)
        # Check that the user_id attribute is present in the response data.
        self.assertTrue("user_id" in response.json()["data"])
        # Check that the name attribute is present in the response data.
        self.assertTrue("name" in response.json()["data"])
        # Check that the country_code attribute is present in the response data.
        self.assertTrue("country_code" in response.json()["data"])
        # Check that the phone_number attribute is present in the response data.
        self.assertTrue("phone_number" in response.json()["data"])
        # Check that the email attribute is present in the response data.
        self.assertTrue(
            "email" not in response.json()["data"]
            or response.json()["data"]["email"] is not None
        )
        # Check that the login_hash attribute is present in the response data.
        self.assertTrue("login_hash" in response.json()["data"])
        # Check that the login_hash_expires_at attribute is present in the response data.
        self.assertTrue("login_hash_expires_at" in response.json()["data"])

    def test_user_login_with_incorrect_password(self):
        # Test case for user login with incorrect password
        url = reverse("login_user")
        data = {
            "country_code": self.country_code,
            "phone_number": self.phone_number,
            "password": self.wrongpassword,
        }
        # Make a POST request to the url with the given data
        response = self.client.post(url, data, format="json")
        # Check that the response status code is 400 BAD REQUEST.
        self.assertEqual(response.status_code, 400)

    def test_user_login_with_non_existent_user(self):
        # Test case for user login with a non-existent user
        url = reverse("login_user")
        data = {
            "country_code": self.country_code,
            "phone_number": self.phone_number_2,
            "password": self.password,
        }
        # Make a POST request to the url with the given data
        response = self.client.post(url, data, format="json")
        # Check that the response status code is 400 BAD REQUEST.
        self.assertEqual(response.status_code, 400)


class SpamTests(APITestCase):
    def setUp(self):
        # Setting up common data for spam tests
        self.country_code = "+91"
        self.phone_number = "8802631740"
        self.password = "Nakul@12345"
        self.phone_number_2 = "9524765741"
        login_response = self.user_login()
        response_dict = login_response.json()
        self.user_id = response_dict["data"]["user_id"]
        login_hash = response_dict["data"]["login_hash"]

        # Define headers for subsequent requests
        self.headers = {
            "HTTP_AUTHORIZATION": f"Bearer {login_hash}",
            "HTTP_USER_ID": self.user_id,
        }

    def user_login(self):
        # Test case for successful user login
        url = reverse("login_user")
        data = {
            "country_code": self.country_code,
            "phone_number": self.phone_number,
            "password": self.password,
        }
        # Make a POST request to the url with the given data
        response = self.client.post(url, data, format="json")
        # Check that the response status code is 200 OK
        self.assertEqual(response.status_code, 200)
        return response

    def test_mark_number_spam_public_access(self):
        # Test case for marking a number as spam
        mark_spam_url = reverse("mark_number_spam")
        data = {
            "country_code": self.country_code,
            "phone_number": self.phone_number_2,
        }

        # Make a POST request to the url with the given data
        response = self.client.post(mark_spam_url, data, format="json")
        # Check that the response status code is 400
        self.assertEqual(response.status_code, 400)

    def test_mark_number_spam(self):
        # Test case for marking a number as spam
        mark_spam_url = reverse("mark_number_spam")
        data = {
            "country_code": self.country_code,
            "phone_number": self.phone_number_2,
        }

        # Make a POST request to the url with the given data
        response = self.client.post(mark_spam_url, data, format="json", **self.headers)
        # Check that the response status code is 200 OK
        self.assertEqual(response.status_code, 200)

        spam_contact = SpamContacts.objects.get(
            country_code=data["country_code"], phone_number=data["phone_number"]
        )
        self.assertIsNotNone(spam_contact)
        self.assertEqual(spam_contact.spam_count, 1)
        user_spam_contact = UserSpammedContacts.objects.get(
            user_id=self.user_id, spam_id=spam_contact.spam_id
        )
        self.assertIsNotNone(user_spam_contact)
        self.assertEqual(user_spam_contact.spam_count, 1)

    def test_mark_own_number_spam(self):
        # Test case to mark the user's own number as spam
        data = {
            "country_code": self.country_code,
            "phone_number": self.phone_number,
        }

        mark_spam_url = reverse("mark_number_spam")
        # Make a POST request to the url with the given data
        response = self.client.post(mark_spam_url, data, format="json", **self.headers)

        # Check that the response status code is 400 BAD REQUEST.
        self.assertEqual(response.status_code, 400)


class SearchTests(APITestCase):
    def setUp(self):
        # Setting up common data for spam tests
        self.country_code = "+91"
        self.phone_number = "8802631740"
        self.password = "Nakul@12345"
        self.phone_number_2 = "9524765741"
        login_response = self.user_login()
        response_dict = login_response.json()
        user_id = response_dict["data"]["user_id"]
        login_hash = response_dict["data"]["login_hash"]

        # Define headers for subsequent requests
        self.headers = {
            "HTTP_AUTHORIZATION": f"Bearer {login_hash}",
            "HTTP_USER_ID": user_id,
        }

    def user_login(self):
        # Test case for successful user login
        url = reverse("login_user")
        data = {
            "country_code": self.country_code,
            "phone_number": self.phone_number,
            "password": self.password,
        }
        # Make a POST request to the url with the given data
        response = self.client.post(url, data, format="json")
        # Check that the response status code is 200 OK
        self.assertEqual(response.status_code, 200)
        return response

    def test_search_by_name_valid(self):
        # Test case for valid search by name
        search_by_name_url = reverse("search_by_name")
        data = {
            "name": "User Name 1",
            "page_no": "1",
            "max_result": "10",
        }

        # Make a POST request to the url with the given data
        response = self.client.post(
            search_by_name_url, data, format="json", **self.headers
        )
        # Check that the response status code is 200 OK
        self.assertEqual(response.status_code, 200)
        # Check that the data attribute is not empty.
        self.assertTrue(len(response.json()["data"]) > 0)
        # Check that the contact_id attribute is present in the response data.
        self.assertTrue("contact_id" in response.json()["data"][0])
        # Check that the name attribute is present in the response data.
        self.assertTrue("name" in response.json()["data"][0])
        # Check that the country_code attribute is present in the response data.
        self.assertTrue("country_code" in response.json()["data"][0])
        # Check that the phone_number attribute is present in the response data.
        self.assertTrue("phone_number" in response.json()["data"][0])
        # Check that the spam_count attribute is present in the response data.
        self.assertTrue("spam_count" in response.json()["data"][0])

    def test_search_by_name_empty_name(self):
        # Test case for search by name with an empty name field
        search_by_name_url = reverse("search_by_name")
        data = {
            "name": "",
            "page_no": "1",
            "max_result": "10",
        }

        # Make a POST request to the url with the given data
        response = self.client.post(
            search_by_name_url, data, format="json", **self.headers
        )

        # Check that the response status code is 400 BAD REQUEST.
        self.assertEqual(response.status_code, 400)

    def test_search_by_name_invalid_page_number_and_max_result(self):
        # Test case for search by name with invalid page number and max results
        search_by_name_url = reverse("search_by_name")
        data = {
            "name": "User Name 1",
            "page_no": "-1",
            "max_result": "0",
        }

        # Make a POST request to the url with the given data
        response = self.client.post(
            search_by_name_url, data, format="json", **self.headers
        )
        # Check that the response status code is 400 BAD REQUEST.
        self.assertEqual(response.status_code, 400)

    def test_search_by_phone_number_valid_registered_user(self):
        # Test case for valid search by phone number
        search_by_phone_url = reverse("search_by_phone_number")
        data = {
            "country_code": self.country_code,
            "phone_number": self.phone_number,
            "page_no": "1",
            "max_result": "10",
        }
        # Make a POST request to the url with the given data
        response = self.client.post(
            search_by_phone_url, data, format="json", **self.headers
        )
        # Check that the response status code is 200 OK
        self.assertEqual(response.status_code, 200)
        # Check that the data attribute is not empty.
        self.assertTrue(len(response.json()["data"]) > 0)
        # Check that the user_id attribute is present in the response data.
        self.assertTrue("user_id" in response.json()["data"][0])
        # Check that the name attribute is present in the response data.
        self.assertTrue("name" in response.json()["data"][0])
        # Check that the country_code attribute is present in the response data.
        self.assertTrue("country_code" in response.json()["data"][0])
        # Check that the phone_number attribute is present in the response data.
        self.assertTrue("phone_number" in response.json()["data"][0])
        # Check that the spam_count attribute is present in the response data.
        self.assertTrue("spam_count" in response.json()["data"][0])

    def test_search_by_phone_number_valid_unregistered_user(self):
        # Test case for valid search by phone number
        search_by_phone_url = reverse("search_by_phone_number")
        data = {
            "country_code": self.country_code,
            "phone_number": self.phone_number_2,
            "page_no": "1",
            "max_result": "10",
        }
        # Make a POST request to the url with the given data
        response = self.client.post(
            search_by_phone_url, data, format="json", **self.headers
        )
        # Check that the response status code is 200 OK
        self.assertEqual(response.status_code, 200)
        # Check that the data attribute is not empty.
        self.assertTrue(len(response.json()["data"]) > 0)
        # Check that the contact_id attribute is present in the response data.
        self.assertTrue("contact_id" in response.json()["data"][0])
        # Check that the name attribute is present in the response data.
        self.assertTrue("name" in response.json()["data"][0])
        # Check that the country_code attribute is present in the response data.
        self.assertTrue("country_code" in response.json()["data"][0])
        # Check that the phone_number attribute is present in the response data.
        self.assertTrue("phone_number" in response.json()["data"][0])
        # Check that the spam_count attribute is present in the response data.
        self.assertTrue("spam_count" in response.json()["data"][0])

    def test_search_by_phone_number_invalid_phone_number(self):
        # Test case for invalid phone number
        search_by_phone_url = reverse("search_by_phone_number")
        data = {
            "country_code": self.country_code,
            "phone_number": "abcd",
            "page_no": "1",
            "max_result": "10",
        }
        # Make a POST request to the url with the given data
        response = self.client.post(
            search_by_phone_url, data, format="json", **self.headers
        )
        # Check that the response status code is 400 BAD REQUEST
        self.assertEqual(response.status_code, 400)

    def test_search_by_phone_number_invalid_page_number_or_max_results(self):
        # Test case for invalid page number or max results
        search_by_phone_url = reverse("search_by_phone_number")
        data = {
            "country_code": self.country_code,
            "phone_number": self.phone_number,
            "page_no": "-1",
            "max_result": "0",
        }
        # Make a POST request to the url with the given data
        response = self.client.post(
            search_by_phone_url, data, format="json", **self.headers
        )
        # Check that the response status code is 400 BAD REQUEST
        self.assertEqual(response.status_code, 400)

    def test_get_detail_by_valid_contact_id_with_email(self):
        # Test case for valid contact ID
        get_detail_url = reverse("detail_by_contact_id")
        contact_id = "5PMkdCInUk7vBUb1biOa4OHpagS7ZjeDK2Nx2kzHJkMECsZQZ_"
        # Make a POST request to the url with the given data
        response = self.client.post(
            get_detail_url,
            {"contact_id": contact_id},
            format="json",
            **self.headers,
        )
        # Check that the response status code is 200 OK
        self.assertEqual(response.status_code, 200)
        # Check that the data attribute is not empty.
        self.assertTrue(len(response.json()["data"]) > 0)
        # Check that the contact_id attribute is present in the response data.
        self.assertTrue("contact_id" in response.json()["data"])
        # Check that the name attribute is present in the response data.
        self.assertTrue("name" in response.json()["data"])
        # Check that the country_code attribute is present in the response data.
        self.assertTrue("country_code" in response.json()["data"])
        # Check that the phone_number attribute is present in the response data.
        self.assertTrue("phone_number" in response.json()["data"])
        # Check that the spam_count attribute is present in the response data.
        self.assertTrue("spam_count" in response.json()["data"])
        # Check that the email attribute is present in the response data.
        self.assertTrue("email" in response.json()["data"])

    def test_get_detail_by_valid_contact_id_without_email(self):
        # Test case for valid contact ID
        get_detail_url = reverse("detail_by_contact_id")
        contact_id = "ewef3CInUk7vBUb1biOa4OHpagS7ZjeDK2Nx2kzHJkMECsssf_"
        # Make a POST request to the url with the given data
        response = self.client.post(
            get_detail_url,
            {"contact_id": contact_id},
            format="json",
            **self.headers,
        )
        # Check that the response status code is 200 OK
        self.assertEqual(response.status_code, 200)
        # Check that the data attribute is not empty.
        self.assertTrue(len(response.json()["data"]) > 0)
        # Check that the contact_id attribute is present in the response data.
        self.assertTrue("contact_id" in response.json()["data"])
        # Check that the name attribute is present in the response data.
        self.assertTrue("name" in response.json()["data"])
        # Check that the country_code attribute is present in the response data.
        self.assertTrue("country_code" in response.json()["data"])
        # Check that the phone_number attribute is present in the response data.
        self.assertTrue("phone_number" in response.json()["data"])
        # Check that the spam_count attribute is present in the response data.
        self.assertTrue("spam_count" in response.json()["data"])
        # Check that the email attribute is not present in the response data.
        self.assertTrue("email" not in response.json()["data"])

    def test_get_detail_by_invalid_contact_id(self):
        # Test case for invalid contact ID
        get_detail_url = reverse("detail_by_contact_id")
        contact_id = "-1"
        # Make a POST request to the url with the given data
        response = self.client.post(
            get_detail_url,
            {"contact_id": contact_id},
            format="json",
            **self.headers,
        )
        # Check that the response status code is 400 BAD REQUEST
        self.assertEqual(response.status_code, 400)

    def test_get_detail_by_none_contact_id(self):
        # Test case for getting details by None contact_id
        get_detail_url = reverse("detail_by_contact_id")
        contact_id = None
        # Make a POST request to the url with the given data
        response = self.client.post(
            get_detail_url,
            {"contact_id": contact_id},
            format="json",
            **self.headers,
        )
        # Check that the response status code is 400 BAD REQUEST
        self.assertEqual(response.status_code, 400)

    def test_get_detail_by_user_id_valid_with_email(self):
        # Test case for getting details by valid user_id
        url = reverse("detail_by_user_id")
        # Make a POST request to the url with the given data
        response = self.client.post(
            url,
            {"user_id": "njbhjy8tr7ytrfdcvbhgfdr657646578iyugfhuyyt54556734"},
            format="json",
            **self.headers,
        )
        # Check that the response status code is 200.
        self.assertEqual(response.status_code, 200)
        # Check that the data attribute is not empty.
        self.assertTrue(len(response.json()["data"]) > 0)
        # Check that the user_id attribute is present in the response data.
        self.assertTrue("user_id" in response.json()["data"])
        # Check that the name attribute is present in the response data.
        self.assertTrue("name" in response.json()["data"])
        # Check that the country_code attribute is present in the response data.
        self.assertTrue("country_code" in response.json()["data"])
        # Check that the phone_number attribute is present in the response data.
        self.assertTrue("phone_number" in response.json()["data"])
        # Check that the spam_count attribute is present in the response data.
        self.assertTrue("spam_count" in response.json()["data"])
        # Check that the email attribute is present in the response data.
        self.assertTrue("email" in response.json()["data"])

    def test_get_detail_by_user_id_valid_without_email(self):
        # Test case for getting details by valid user_id
        url = reverse("detail_by_user_id")
        # Make a POST request to the url with the given data
        response = self.client.post(
            url,
            {"user_id": "bhkscnkvgusdhuiygushbjdsgd762374yighjwfdsgdsdf534w"},
            format="json",
            **self.headers,
        )
        # Check that the response status code is 200 OK
        self.assertEqual(response.status_code, 200)
        # Check that the data attribute is not empty.
        self.assertTrue(len(response.json()["data"]) > 0)
        # Check that the user_id attribute is present in the response data.
        self.assertTrue("user_id" in response.json()["data"])
        # Check that the name attribute is present in the response data.
        self.assertTrue("name" in response.json()["data"])
        # Check that the country_code attribute is present in the response data.
        self.assertTrue("country_code" in response.json()["data"])
        # Check that the phone_number attribute is present in the response data.
        self.assertTrue("phone_number" in response.json()["data"])
        # Check that the spam_count attribute is present in the response data.
        self.assertTrue("spam_count" in response.json()["data"])
        # Check that the email attribute is not present in the response data.
        self.assertTrue("email" not in response.json()["data"])

    def test_get_detail_by_user_id_invalid(self):
        # Test case for getting details by invalid user_id
        url = reverse("detail_by_user_id")
        # Make a POST request to the url with the given data
        response = self.client.post(
            url, {"user_id": "shbfksbhfskdsf"}, format="json", **self.headers
        )
        # Check that the response status code is 400 BAD REQUEST
        self.assertEqual(response.status_code, 400)

    def test_get_detail_by_user_id_none(self):
        # Test case for getting details by None user_id
        url = reverse("detail_by_user_id")
        # Make a POST request to the url with the given data
        response = self.client.post(
            url, {"user_id": None}, format="json", **self.headers
        )
        # Check that the response status code is 400 BAD REQUEST
        self.assertEqual(response.status_code, 400)
