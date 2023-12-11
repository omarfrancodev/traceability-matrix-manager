from rest_framework.permissions import BasePermission
from django.contrib.auth import get_user_model
from eventrecord.models import EventRecord

from project.models import Project
from record.models import Record

User = get_user_model()
grp = " Group";

class AdminPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name=User.Role.Admin + grp).exists()

class TeamMemberPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name=User.Role.TeamMember + grp).exists()
    
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Project):
            return obj.assignedUsers.filter(id=request.user.id).exists()
        elif isinstance(obj, Record):
            project = obj.associatedProject
            return project.assignedUsers.filter(id=request.user.id).exists()
        elif isinstance(obj, EventRecord):
            return True
        return False
    
class GuestPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name=User.Role.Guest + grp).exists()
        
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Project):
            return obj.assignedUsers.filter(id=request.user.id).exists()
        elif isinstance(obj, Record):
            project = obj.associatedProject
            return project.assignedUsers.filter(id=request.user.id).exists()
        elif isinstance(obj, EventRecord):
            return True
        return False
