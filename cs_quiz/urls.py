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
from gemini_app import views

# Definir las URLs de la aplicación gemini_app
gemini_app_patterns = [
    path('', views.index, name='index'),
    path('next-question/', views.next_question, name='next_question'),
    path('api/', views.gemini_request, name='gemini_api'),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),  # Usar la vista index como página principal
    path('quiz/', include((gemini_app_patterns, 'gemini_app'), namespace='cs_quiz')),
]

# Añadir configuración de archivos estáticos en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
