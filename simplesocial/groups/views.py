from typing import Any
from django.shortcuts import render , get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse
from django.views import generic
from groups.models import Group, GroupMember
from django.contrib import messages
from . import models

# Create your views here.
class CreateGroup(LoginRequiredMixin,generic.CreateView):
    fields = ('name','description')
    model = Group

class SingleGroup(generic.DetailView):
    model = Group 

class ListGroups(generic.ListView):
    model = Group

class JoinGroup(LoginRequiredMixin, generic.RedirectView):
    def get_redirect_url(self, *args, **kwarg):
        return reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')})
    def get(self,request, *args, **kwarg):
        group = get_object_or_404(Group,slug=self.kwargs.get('slug'))
        try:
            GroupMember.objects.create(user=self.request.user, group=group)
        except :
            messages.warning(self.request,"Already a member")
        else:
            messages.success(self.request,'You are now a member.')
        return super().get(request,*args,**kwarg)


class LeaveGroup(LoginRequiredMixin,generic.RedirectView):
    def get_redirect_url(self, *args, **kwarg):
        return reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')})
    def get(self,request, *args, **kwarg):
        try:
            membership = models.GroupMember.objects.filter(
                user = self.request.user,
                group__slug = self.kwargs.get('slug')
            ).get()
        except: 
            messages.warning(self.request,"Not in this Group")
        else:
            membership.delete()
            messages.success(self.request,"Left group")
        return super().get(request,*args,**kwarg)