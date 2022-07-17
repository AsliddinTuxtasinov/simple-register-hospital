from django.urls import path
from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("logout", views.LogoutView.as_view(), name="logout"),
    path("login", views.LoginView.as_view(), name="login"),
    path("register", views.CreateDiseasedView.as_view(), name="register"),
    path("create/doctor", views.CreateDoctorView.as_view(), name="create_doctor"),
    path("detail/<int:pk>", views.DetailPageView.as_view(), name="detail"),
    path("<int:pk>/goto/doctor", views.GotoDoctorView.as_view(), name="goto-doctor"),
    path("<int:diseased_id>/status/diseased/user", views.CreateStatusDiseasedUserView.as_view(),
         name="status-diseased-user"),
    path("profile", views.AdminDashboardView.as_view(), name="profile"),

]
