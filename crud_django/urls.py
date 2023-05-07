# from rest_framework import routers
from django.urls import path
from . import views
# from .views import StudentView

# router = routers.DefaultRouter()
# router.register('', StudentView)

# router.register('', get)
# urlpatterns = router.urls

urlpatterns = [
    path('api/process_text/', views.process_text, name='process_text'),
    
]