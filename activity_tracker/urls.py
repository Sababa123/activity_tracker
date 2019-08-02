"""activity_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
from track.views import (
    get_records,
    add_activity,
    add_category,
    category,
    edit_category,
    delete_category,
    custom_category,
    delete_activity
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('get_activity/', get_records),
    path('activity/', add_activity),
    path('category/', add_category),
    path('get_category/', category),
    path('custom_category/', custom_category),
    path('edit_category/', edit_category),
    path('delete_category/', delete_category),
    path('delete_activity/', delete_activity)
]
