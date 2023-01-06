from django.contrib import admin
from django.urls import path
from api import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/gettokens', views.gettokens),
    path('api/getcandidates', views.get_candidates),
    path('api/vote', views.vote),
    path('api/check/<str:user_token>/', views.check),
    # path('api/page/<str:user_token>/', views.page),
    path('api/getfaculty', views.get_faculty),
    path('api/getvotings', views.get_votings),
    path('thanks/', views.thanks)
]
