from django.contrib import admin
from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token
from api.views import create_user, verify_user, modify_user, google_user

# fmt: off
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    path('auth/login/', obtain_jwt_token),
    path('auth/userinfo/', verify_jwt_token),
    path('auth/signup/', create_user),
    path('auth/verify/', verify_user),
    path('auth/modify/', modify_user),
    path('auth/google', google_user)
]
# fmt: on
