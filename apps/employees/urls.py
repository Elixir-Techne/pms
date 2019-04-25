from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

app_name = "employees"

urlpatterns = [
    path('profile/image', views.set_profile_image, name='profile_image'),
    path('profile/search', views.search_employee, name='search_employee'),
    path('profile/details', views.employee_details, name='employee_details'),
]

router = DefaultRouter()
router.register('profile', views.EmployeeProfileView, 'profile')
router.register('employment', views.EmploymentCompensationView, 'employment_compensation')
router.register('bank', views.BankView, 'bank')
router.register('paycheck', views.PaycheckView, 'paycheck')
urlpatterns = urlpatterns + router.urls
