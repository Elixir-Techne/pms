from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

urlpatterns = [
    path('my-tasks', views.get_my_project_tasks, name='my_project_tasks')
]

app_name = 'tasks'

router = DefaultRouter()
router.register(r'task/category', views.CategoryView, 'category')
router.register(r'task', views.TaskView, 'tasks')

urlpatterns = urlpatterns + router.urls
