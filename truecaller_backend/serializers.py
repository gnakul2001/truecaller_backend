from rest_framework import serializers
from .models import *
from .helper import encrypt_string, generate_random_string


# Serializer for User model
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "user_id",
            "name",
            "country_code",
            "phone_number",
            "email",
            "password",
            "login_hash",
            "login_hash_expires_at",
        )
        extra_kwargs = {
            "password": {"write_only": True},  # Password field is write-only
            "user_id": {"required": False},
        }

    def create(self, validated_data):
        # Handling password encryption and user_id generation during user creation
        password = validated_data.pop("password")
        hashed_password = encrypt_string(password)  # Encrypt the password
        user_id = generate_random_string(50)  # Generate a random user ID
        user = User.objects.create(
            user_id=user_id, password=hashed_password, **validated_data
        )
        return user

    def validate_phone_number(self, value):
        # Custom validation to ensure phone number uniqueness
        if User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError(
                "Someone with this phone number already exists."
            )
        return value


# Serializer for Contacts model
class ContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = (
            "user_id_imported_contacts",
            "name",
            "country_code",
            "phone_number",
        )


# Serializer for SpamContacts model
class SpamContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpamContacts
        fields = ("spam_id", "country_code", "phone_number", "spam_count")


# Serializer for UserSpammedContacts model
class UserSpammedContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSpammedContacts
        fields = ("user_id", "spam_id", "spam_count")
