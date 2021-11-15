from django.urls import include, path
from . import views

urlpatterns = [
    path('auth/', include('rest_auth.urls')),    
    path('auth/register/', include('rest_auth.registration.urls')),
    path('contacts/<int:username_id>/', views.contacts, name="contact"),
    path('new_contact/', views.new_contact, name="new_contact"),
    path('contact/<int:contact_id>/', views.profile_contact, name="profile_contact"),
    path('plans/', views.plans, name="plans"),
    path('new_customer/', views.new_customer, name="new_customer"),
    path('customers/<int:username_id>/', views.customers, name="customers"),
    path('customer/<int:contact_id>/', views.customer, name="customer"),
    path('edit_contact/<int:contact_id>/', views.edit_contact, name="edit_contact"),
    path('edit_customer/<int:customer_id>/', views.edit_customer, name="edit_customer"),
    path('graph_contacts/<int:username_id>/', views.graph_contacts, name="graph_contacts"),
    path('related_plans/<int:username_id>/', views.related_plans, name="related_plans"),
    path('', views.mensaje, name="mensaje")
]