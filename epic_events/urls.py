"""epic_events URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.db import router
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from django.views.generic import RedirectView, TemplateView
from users.urls import router as user_router
from clients.urls import router as client_router
from contracts.urls import router as contract_router
from events.urls import router as event_router

router = SimpleRouter()
router.registry.extend(user_router.registry)
router.registry.extend(client_router.registry)
router.registry.extend(contract_router.registry)
router.registry.extend(event_router.registry)

urlpatterns = [
    path('admin/', admin.site.urls, name="admin"),
    path('authentification/', include('rest_framework.urls')),
    path('', include(router.urls)),
    
]

    # path("accounts/profile/", auth_views.LoginView.as_view(template_name="registration/login.html")),
    # path("accounts/profile/", TemplateView.as_view(template_name="registration/login.html")),
    # path("authentification/login/", TemplateView.as_view(url="/authentification/login/")),
    # path("authentification/logout/", RedirectView.as_view(url="/authentification/logout/")),
    # path("authentification/logout/?next=/users/", RedirectView.as_view(url="/authentification/logout/")),