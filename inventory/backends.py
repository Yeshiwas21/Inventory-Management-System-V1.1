from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, user_type=None, **kwargs):
        UserModel = get_user_model()

        try:
            user = UserModel.objects.get(username=username, user_type=user_type)
        except UserModel.DoesNotExist:
            print(f"User with username {username} and user_type {user_type} doesn't exist")
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            print(f"User with username {username} and user_type {user_type} authenticated successfully")
            return user
        else:
            print(f"Authentication failed for user with username {username} and user_type {user_type}")
            return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
