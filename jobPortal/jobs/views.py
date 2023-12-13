from typing import Any
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render,redirect, get_object_or_404
from django.views.generic import (ListView,
                                  CreateView,
                                  DetailView,
                                  UpdateView,
                                  DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Jobs
from chats.models import *
from django.contrib.auth.models import User
import json
from django.http import JsonResponse



# Create your views here.
class JobsListView(LoginRequiredMixin,ListView):
    model = Jobs
    #template name = '<app>/<model>_<viewType>.html'    

    def get_queryset(self):
        user_id = self.kwargs.get('user_id') #this self.kwargs.get will get value which you passed in url
        user_type = self.request.user.profile.user_type
        if user_id and user_type =='R':
            print(user_type)
            return Jobs.objects.filter(recruiter=user_id)
        else:
            return Jobs.objects.all()


class JobsCreateView(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    model=Jobs
    fields = ['job_title',
                  'job_type',
                  'location',
                  'pay_per_day',
                  'gender_preference',
                  'date_of_event',
                  'start_time',
                  'end_time',
                  'age_limit',
                  'duration_of_event',
                  'shift',
                  'dress_code',
                #   'whatsapp_link',
                  'description']

    def form_valid(self, form):
        form.instance.recruiter = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        # job = self.get_object()
        if self.request.user.profile.user_type == 'R':
            return True
        else:
            False
    


class JobDetailView(LoginRequiredMixin,DetailView):
    model = Jobs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['custom_dress_code'] = self.object.get_dress_code_display()
        context['custom_shift'] = self.object.get_shift_display()
        context['custom_gender_preference'] = self.object.get_gender_preference_display()
        return context
    
    def post(self,request,*args, **kwargs):
        if request.method == 'POST':
            data = json.loads(request.body)
            jobId = data['job']
            userId = data['user']
            user = User.objects.get(id=userId)
            job = Jobs.objects.get(id=jobId)
            joinRequestChat = JoinRequestChatroom.objects.filter(user=user,job=job).exists()
            if not joinRequestChat:
                JoinRequestChatroom.objects.create(user=user,job=job)
            else:
                return redirect('jobs-detail', pk=jobId)

            

        return redirect('jobs-detail', pk=jobId)
        # return render(request,'jobs/jobs_detail.html' ,{'job':job})
    

class JobUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Jobs
    fields = ['job_title',
                  'job_type',
                  'location',
                  'pay_per_day',
                  'gender_preference',
                  'date_of_event',
                  'start_time',
                  'end_time',
                  'age_limit',
                  'duration_of_event',
                  'shift',
                  'dress_code',
                #   'whatsapp_link',
                  'description']

    



    def form_valid(self,form):
        form.instance.recruiter = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        job = self.get_object()
        return self.request.user == job.recruiter
    


class JobDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Jobs
    success_url = '/'
    #it takes template '<model>_confirm_delete.html' and you have to provide form 
    #the form says confirm delete and submit button to delete 

    def test_func(self):
        job = self.get_object()
        return self.request.user == job.recruiter
    

class AppliedUserView(LoginRequiredMixin,ListView):
    model = JoinRequestChatroom
    template_name = 'jobs/applied_user.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['jobs_id'] =self.kwargs.get('jobs_id')
        return context
    
    def post(self,request, *args,**kwargs):
        if request.method == 'POST':
            data = json.loads(request.body)
            userId = data['userId']
            jobsId = data['jobId']
            status = data['status']
            # Retrieve instances of Jobs and User models using IDs
            userInstance = get_object_or_404(User, id=userId)
            jobInstance = get_object_or_404(Jobs, id=jobsId)
            checkUserExist = ChatGroupMember.objects.filter(group=jobInstance, member = userInstance).exists()
            if status == 'accept' and not checkUserExist:
                ChatGroupMember.objects.create(group=jobInstance,member=userInstance)
                try:
                    joinRequest = JoinRequestChatroom.objects.get(user=userId,job=jobsId)
                    print(joinRequest)
                    joinRequest.delete()
                    return redirect('applied-user', jobs_id = jobsId)
                except:
                    pass
            else:
                joinRequest = JoinRequestChatroom.objects.get(user=userId,job=jobsId)
                print(joinRequest)
                joinRequest.delete()




            print(data)
            return redirect('applied-user', jobs_id = jobsId)