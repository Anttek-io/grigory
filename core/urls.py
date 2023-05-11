"""grigory URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView

from core.api.views import SpectacularRapiDocView
from core.settings import REST_EXPOSE_AUTH_API, BASE_PATH, EXPOSE_DEMO_SITE

urlpatterns = [
    path(BASE_PATH + 'admin/', admin.site.urls),
    path(BASE_PATH + 'api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path(BASE_PATH + 'api/docs/', SpectacularRapiDocView.as_view(url_name='schema'), name='docs'),
]

if REST_EXPOSE_AUTH_API:
    urlpatterns += [
        path(BASE_PATH + 'api/auth/', include('authentication.api.urls'), name='authentication'),
    ]

urlpatterns += [
    path(BASE_PATH + 'api/', include('app.api.urls'))
]

if EXPOSE_DEMO_SITE:
    urlpatterns += [
        path(BASE_PATH + '', include('demo.urls'))
    ]
