"""
URL configuration for treasure_hunt_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from rest_framework import routers
from .views import TreasureViewSets, ProfileViewSets, DeleteUserView, CreateUserView, UpdateUserView

router = routers.DefaultRouter()
router.register(r'treasure', TreasureViewSets)
router.register(r'users', ProfileViewSets)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('users/<int:pk>/', DeleteUserView.as_view(), name='delete-user'),
    path('users', CreateUserView.as_view(), name="create-user"),
    path('users/<int:pk>/', UpdateUserView.as_view(), name="update-user")
]

urlpatterns += router.urls