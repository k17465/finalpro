"""finalpro URL Configuration

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
from finalpro.settings import DEBUG
if DEBUG:
    import debug_toolbar
from django.conf.urls import include
from report.views import index, get_user, list_view, register, login_view, logout_view
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index, name="index"),
    # path("redirect", redirect_test),
    path("register", register, name="register"),
    path("login", login_view, name = "login"),
    path("logout", logout_view, name = "logout"),
    path("users", list_view, name="list_view"),
]

if DEBUG:
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),  #Django Debug Toolbar
    ]