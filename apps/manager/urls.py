from rest_framework.routers import DefaultRouter

from . import views

urlpatterns = []

app_name = 'managers'

router = DefaultRouter()
router.register(r'', views.ManagerView, 'managers')

urlpatterns = urlpatterns + router.urls
