"""
URL configuration for cs_quiz project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.conf.urls.static import static
from django.shortcuts import redirect
from gemini_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('submit_answer/', views.submit_answer, name='submit_answer'),
    path('next_question/', views.next_question, name='next_question'),
    path('get_metrics/', views.get_metrics, name='get_metrics'),
    path('reset_metrics/', views.reset_metrics, name='reset_metrics'),
    path('clear_session/', views.clear_session, name='clear_session'),
    path('refresh/', lambda request: redirect('/?refresh=1'), name='refresh'),
]

# Añadir configuración de archivos estáticos en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
