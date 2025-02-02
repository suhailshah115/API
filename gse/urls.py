from django.urls import path
from .views import get_contact , resolve_contact, home_view

urlpatterns = [


        path('', home_view, name='home'),
        path('contact/', get_contact, name ='get_contact') ,   
        path('resolve-contact', resolve_contact, name= 'resolve-contact')       
]