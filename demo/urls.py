from django.urls import path, include
from demo import views as demo_views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path("", demo_views.chat_page, name="chat-page"),

    # login-section
    path("auth/login/", LoginView.as_view(template_name="demo/login_page.html"), name="demo-login"),
    path("auth/logout/", LogoutView.as_view(), name="demo-logout"),
]
