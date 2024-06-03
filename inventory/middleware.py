from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.db import transaction

class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    @transaction.atomic
    def __call__(self, request):
        response = self.get_response(request)

        authenticated_user = request.user.is_authenticated
        access_to_protected_view = request.path in [reverse('product_list'), reverse('user_list')]

        if not authenticated_user and access_to_protected_view:
            messages.error(request, 'You must be logged in to access this page.')
            return redirect('login')

        return response
