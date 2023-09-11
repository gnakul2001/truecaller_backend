from django.urls import path
from truecaller_backend.views.user import *
from truecaller_backend.views.actions import *
from truecaller_backend.views.search import *
from truecaller_backend.views.home_view import *
from django.contrib import admin

urlpatterns = [
    # Home view, accessible at the root URL
    path(
        "",
        HomeView.as_view(),
        name="home",
    ),
    # User registration view, accessible at "/user/create"
    path(
        "user/create",
        UserRegister.as_view(),
        name="create_user",
    ),
    # User login view, accessible at "/user/login"
    path(
        "user/login",
        UserLogin.as_view(),
        name="login_user",
    ),
    # Mark number as spam view, accessible at "/actions/make_number_spam"
    path(
        "actions/make_number_spam",
        MarkNumberSpam.as_view(),
        name="mark_number_spam",
    ),
    # Search contacts by name, accessible at "/search/by_name"
    path(
        "search/by_name",
        SearchByName.as_view(),
        name="search_by_name",
    ),
    # Search contacts by phone number, accessible at "/search/by_phone_number"
    path(
        "search/by_phone_number",
        SearchByPhoneNumber.as_view(),
        name="search_by_phone_number",
    ),
    # Get contact details by contact_id, accessible at "/search/details/contact_id"
    path(
        "search/details/contact_id",
        GetDetailByContactId.as_view(),
        name="detail_by_contact_id",
    ),
    # Get contact details by user_id, accessible at "/search/details/user_id"
    path(
        "search/details/user_id",
        GetDetailByUserId.as_view(),
        name="detail_by_user_id",
    ),
]
