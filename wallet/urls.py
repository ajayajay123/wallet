"""wallet URL Configuration

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
from django.urls import path, include
from rest_framework import routers
from walletapp import views as walletapp_view

router = routers.SimpleRouter()
# router.register(r'/', walletapp_view.home)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', walletapp_view.home),
    # path('operation/', walletapp_view.operation),
    path('dashboard', walletapp_view.dashboard),
    path('home/', walletapp_view.home),
    path('operation/', walletapp_view.operation_api),
    # Callback
    path('callback/', walletapp_view.callback_of_server),
    path('setup-user/', walletapp_view.setup_user_callback),
    path('setup-deploy/', walletapp_view.setup_deploy_callback),
    path('setup-execute/', walletapp_view.setup_execute_callback),

    # Api
    path('api/', walletapp_view.home_api),
    path('get-key_api/', walletapp_view.get_key_api),
    path('operation-api/', walletapp_view.operation_api),
]
