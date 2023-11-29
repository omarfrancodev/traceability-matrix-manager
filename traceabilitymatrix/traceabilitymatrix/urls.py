"""
URL configuration for traceabilitymatrix project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.views.static import serve

apiVersion = 'api/v1/'

urlpatterns = [
    path(apiVersion + 'admin/', admin.site.urls),
    path(apiVersion + 'auth/', include ('authuser.urls')),
    path(apiVersion + 'users/', include ('user.urls')),
    path(apiVersion + 'projects/', include ('project.urls')),
    path(apiVersion + 'records/', include ('record.urls')),
    path(apiVersion + 'media/<path:path>/', serve, {'document_root': settings.MEDIA_ROOT}),
]
