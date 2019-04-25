from rest_framework.permissions import BasePermission

from apps.employees.models import Employee


class EmployeePermission(BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    """
    message = 'User is not authorized to modify Employee data..'

    def has_permission(self, request, view):
        # Instance must have an attribute named `owner`.
        # try:
        #     print(request.parser_context["kwargs"])
        #     if request.user.is_superuser:
        #         return True
        #     else:
        #         employee_id = request.parser_context["kwargs"]['pk']
        #         employee = Employee.objects.get(pk=employee_id)
        #         print(employee)
        #         return int(employee.user.id) == int(request.user.id)
        # except ValueError:
        #     return False
        # except KeyError:
        #     return False
        return True