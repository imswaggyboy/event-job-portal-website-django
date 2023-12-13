from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from .models import *
from django.contrib.auth.models import User
from jobs.models import *


# Create your views here.
# class MyChats(DetailView):
#     model = ChatGroup
    #template name = '<app>/<model>_<viewType>.html'  



@login_required
def MyChats(request,pk):
    # user = User.objects.get(user=request.user)
    user = request.user
    jobGroup = Jobs.objects.filter(id=pk).first()
    chatMember = get_object_or_404(ChatGroupMember, group=pk,member=user)
    print(chatMember)
    # chats = []
    chats = ChatGroup.objects.filter(job=pk)


    return render(request , 'chats/chats_detail.html', {'job':jobGroup , 'chats':chats }) 

@login_required
def message_list(request):
    user = request.user
    chat_groups = ChatGroupMember.objects.filter(member=user)
    print(chat_groups)

    return render(request , 'chats/message_list.html', {'chat_groups': chat_groups})