from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the attacker.
        return obj.owner == request.user


class IsOwnerOrVictim(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed only to owners or victims connected to the attacker,
        # so we'll allow GET, HEAD or OPTIONS to those requests.
        if request.method in permissions.SAFE_METHODS and (
                obj.owner == request.user or obj.victim.owner == request.user):
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user
