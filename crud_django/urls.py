from rest_framework import routers

from .views import StudentView

router = routers.DefaultRouter()
router.register('', StudentView)
urlpatterns = router.urls