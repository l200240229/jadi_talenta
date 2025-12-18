from django.urls import path
from .views import profile_me, public_talent_list, public_talent_detail,public_talent_latest, download_cv, admin_profile_list, admin_toggle_profile,delete_my_profile


urlpatterns = [
    path("me/", profile_me, name="profile-me"),
    path("me/delete/", delete_my_profile),
    path("public/talents/", public_talent_list),
    path("public/talents/<str:username>/", public_talent_detail),
    path("public-talents/latest/", public_talent_latest),
    path("profiles/me/cv/", download_cv),
    path("admin/profiles/", admin_profile_list),
    path("admin/profiles/<int:profile_id>/toggle/", admin_toggle_profile),
]