from django.urls import path
from . import views

urlpatterns = [
	path("", views.index, name="index"),
	path("join-group/<uuid:group_id>/", views.add_to_group, name="join_group"),
	path("group/chat/<uuid:group_id>/", views.view_group, name="view_chat"),
	path("create_group/", views.create_group, name="create_group"),
	path("signup/", views.signup, name="signup"),
	path("signin/", views.signin, name="signin"),
	path("logout/", views.logout, name="logout"),
]
