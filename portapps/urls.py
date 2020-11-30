from django.urls import path
from .views import *

urlpatterns = [
    path('', ContactView),
    path('email/', contact),
    path('excel/', excel),
]
