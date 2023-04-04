"""msforms URL Configuration

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
from django.urls import path,include
from listings import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('importation/', views.importation, name='importation'),
    path('analyse/', views.analyse, name='analyse'),
    path('exportation/', views.exportation, name='exportation'),
    path('analyse_erreur/', views.not_upload, name='not-upload'),
    path('exportation/pdf', views.pdf_view, name='pdf'),

]
