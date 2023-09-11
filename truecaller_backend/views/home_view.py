from django.http import HttpResponse
from rest_framework.views import APIView


class HomeView(APIView):
    def get(self, request, format=None):
        return HttpResponse("<h1>TrueCaller Clone by Nakul Gupta</h1>")
