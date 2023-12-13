from django.urls import path
from .views import *

urlpatterns = [
    path('<int:pk>/',MyChats,name='chats'), #template name = '<app>/<model>_<viewType>.html'    
    path('messages/',message_list,name='message-list'), #template name = '<app>/<model>_<viewType>.html'    
]
