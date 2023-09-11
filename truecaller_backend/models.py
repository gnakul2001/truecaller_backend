from django.db import models

# Create your models here.


# This Model will save the user data and fetch from the DB.
class User(models.Model):
    user_id = models.CharField(max_length=100)  # User Id of the registered user.
    name = models.CharField(max_length=100)  # Name of the registered user.
    country_code = models.CharField(
        max_length=15
    )  # Country Code of the registered user.
    phone_number = models.BigIntegerField()  # Phone Number of the registered user.
    email = models.EmailField(blank=True, null=True)  # Email of the registered user.
    password = models.CharField(max_length=150)  # Password of the registered user.

    # Login Hash of the registered user. Used to check if
    # the user logined is genuine or someone else sending user_id in request.
    login_hash = models.CharField(max_length=500, blank=True, null=True)
    login_hash_expires_at = models.DateTimeField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(
        auto_now_add=True
    )  # Automatically set when the object is first created.
    updated_at = models.DateTimeField(
        auto_now=True
    )  # Automatically updated whenever the object is saved.


# This Model will save the contacts data and fetch from the DB.
class Contacts(models.Model):
    contact_id = models.CharField(max_length=100)  # Contact Id of the contact.
    user_id_imported_contacts = models.CharField(
        max_length=100
    )  # User Id of the registered user. This will tell us that this contact is imported by this user_id device
    name = models.CharField(max_length=100)  # Name of the contact.
    country_code = models.CharField(max_length=15)  # Country Code of the contact.
    phone_number = models.BigIntegerField()  # Phone Number of the contact.
    created_at = models.DateTimeField(
        auto_now_add=True
    )  # Automatically set when the object is first created.
    updated_at = models.DateTimeField(
        auto_now=True
    )  # Automatically updated whenever the object is saved.


# This Model will save the spam contacts data and fetch from the DB.
class SpamContacts(models.Model):
    spam_id = models.CharField(max_length=100)  # Spam Id of the spammed contact.
    country_code = models.CharField(max_length=15)  # Country Code of the contact.
    phone_number = models.BigIntegerField()  # Phone number of the contact.
    spam_count = models.IntegerField(default=1)  # Spam count of the contact.
    created_at = models.DateTimeField(
        auto_now_add=True
    )  # Automatically set when the object is first created.
    updated_at = models.DateTimeField(
        auto_now=True
    )  # Automatically updated whenever the object is saved.


# This Model will save the user id of the user that mark spam to the user and spam id.
class UserSpammedContacts(models.Model):
    user_id = models.CharField(max_length=100)  # User Id of the registered user.
    spam_id = models.CharField(max_length=100)  # Spam Id of the spammed contact.
    spam_count = models.IntegerField(default=1)  # Spam count of the contact.
    created_at = models.DateTimeField(
        auto_now_add=True
    )  # Automatically set when the object is first created.
    updated_at = models.DateTimeField(
        auto_now=True
    )  # Automatically updated whenever the object is saved.
