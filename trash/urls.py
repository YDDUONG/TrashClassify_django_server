"""trash URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from trash import views
from trash import views_for_review
from django.conf.urls import include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('signin/', views.signin),
    path('signup/', views.signup),
    path('modify/', views.modify),
    path('update/', views.update),
    path('retrive/', views.retrive),

    path('review_index/', views_for_review.review),
    path('review_login/', views_for_review.login),
    path('review_logout/', views_for_review.logout),

    path('captcha/', include('captcha.urls')),
]
