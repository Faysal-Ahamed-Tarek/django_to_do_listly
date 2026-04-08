from rest_framework import routers

from listly_app.viewsets import tasksViewSet


router = routers.SimpleRouter()
router.register('tasks', tasksViewSet, basename='task')

urlpatterns = router.urls