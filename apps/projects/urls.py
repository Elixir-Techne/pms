from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

urlpatterns = [
    path('my-projects', views.get_my_projects, name='my_projects')
]

app_name = 'projects'

router = DefaultRouter()
router.register(r'customers', views.CustomerView, 'customers')
router.register(r'employees', views.ProjectEmployeeView, 'projects_employees')
router.register(r'', views.ProjectView, 'projects')

urlpatterns = urlpatterns + router.urls
