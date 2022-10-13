"""CsharpCon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include, re_path
from django.contrib.staticfiles.views import serve as serve_static
from CSharpConWallet import views

# Django admin customization
admin.site.site_header = "CSharp Administration"
admin.site.site_title = "CSharp Admin"
admin.site.title = "Dashboard"
admin.site.index_title = "Welcome to Admin Portal"


def _static_butler(request, path, **kwargs):
    return serve_static(request, path, insecure=True, **kwargs)


urlpatterns = [
    path("admin/CSharpConWallet/recentactions", views.recent_actions, name="recent_actions"),
    path("admin/", admin.site.urls),
    path("", include("CSharpConWallet.urls")),
    re_path(r"static/(.+)", _static_butler),
]
