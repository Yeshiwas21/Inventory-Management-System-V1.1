# urls.py
from django.urls import path
from .views import register_user, index, user_list, custom_login, custom_logout, edit_user, DeleteUserView

urlpatterns = [
    # other paths...
    path('', index, name='index'),
    path('login/', custom_login, name='login'),
    path('logout/', custom_logout, name='logout'),
    path('register_user/', register_user, name='register_user'),
    path('edit-user/<int:user_id>/', edit_user, name='edit_user'),
    path('delete-user/<int:user_id>/', DeleteUserView.as_view(), name='delete_user'),
    path('user_list/', user_list, name='user_list'),
]