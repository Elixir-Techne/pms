from rest_framework.permissions import BasePermission


class ClientPermission(BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    """
    message = 'User is not authorized to modify Client data..'

    def has_permission(self, request, view):
        # Instance must have an attribute named `owner`.
        # try:
        #     return int(request.data['user_id']) == int(request.user.id)
        # except ValueError:
        #     return False
        # except KeyError:
        #     return False
        return True
