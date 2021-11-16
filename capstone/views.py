from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from . models import *
from . serializers import *
from datetime import datetime

from django.http import JsonResponse
import json
import pandas as pd
import numpy as np

# Create your views here.

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def contacts(request, username_id):
    # Get all contacts of a specific user
    if request.method == 'GET':
        user = User.objects.get(id = username_id)
        contacts = user.creador.all()
        data = contacts.order_by("-timestamp").all()
        serializer = GetContactSerializer(data, context={'request': request}, many=True)
        print(request)
        return Response({'contacts':serializer.data})

@api_view(['GET'])
def graph_contacts(request, username_id):
    if request.method == 'GET':
        user = User.objects.get(id = username_id)
        contacts = user.creador.all()
        data = contacts.order_by("timestamp").all()
        serializer = GetContactSerializer(data, context={'request': request}, many=True)
        for x in serializer.data:
            x['one'] = 1
            df = pd.DataFrame(serializer.data)
            acumulado = list(df.cumsum()['one'])
            cleanedList = [y for y in acumulado if y == y]
            print(cleanedList[-1])
            x['TotalContacts'] = cleanedList[-1]
        return Response({'contacts':serializer.data})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_contact(request):
    # A new contact must be via POST
    if request.method == 'POST':
        serializer = ContactSerializer(data = request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            contact = Contact.objects.filter(name=name).first()
            if contact == None:
                print(contact)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return JsonResponse({"message": "Contact already exists"}, status=400)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def plans(request):
    # Get all plans
    if request.method == 'GET':
        data = PlanSeguro.objects.all()
        print(data)
        serializer = PlanSeguroSerializer(data, context={'request': request}, many=True)
        return Response({'plans':serializer.data})
    
    # A new plan must be via POST
    elif request.method == 'POST':
        serializer = PlanSeguroSerializer(data = request.data)

        if serializer.is_valid():
            plan = serializer.validated_data.get('plan')
            planSeguro = PlanSeguro.objects.filter(plan=plan).first()
            if planSeguro == None:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return JsonResponse({"message": "Plan already exists"}, status=400)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Get information from a specific contact
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_contact(request, contact_id):
    if request.method == 'GET':
        contact = Contact.objects.get(id = contact_id)
        print(contact)
        serializer = GetContactSerializer(contact, context={'request': request})
        return Response({'contact':serializer.data})
        

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_customer(request):
    if request.method == 'POST':
        serializer = CustomerSerializer(data = request.data)
        if serializer.is_valid():
            #contact_id = serializer.data['contacto']
            contact = serializer.validated_data.get('contacto')
            customer = Customer.objects.filter(contacto =contact).first()
            if customer ==None:
                #customer = Customer.objects.create(contacto =contact)
                contact.iscustomer = True
                contact.save()
                serializer.save()
                return Response({"message": "Customer created successfully!"}, status=status.HTTP_201_CREATED)
            else:
                return JsonResponse({"message": "Customer already exists!"}, status=400)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def customers(request, username_id):
    if request.method == 'GET':
        user = User.objects.filter(id = username_id).first()
        contacts = user.creador.all()
        customers = []
        for contact in contacts:
            customer = contact.info_contact.all().first()
            if customer !=None:
                customers.append(customer)
                #print(customer.planes.all())
                #print(customer.contacto)
        serializer = GetCustomerSerializer(customers, context={'request': request}, many= True)
        sorted_q = sorted(serializer.data, key=lambda fecha: datetime.strptime(fecha['timecustomer'], '%d %b %Y, %I:%M %p'))
        # Go through each client
        for x in sorted_q:
            profit = []
            rate = [
                {'age':20, 'rate':1.21}, 
                {'age':30, 'rate':1.27}, 
                {'age':40, 'rate':1.46},
                {'age':50, 'rate':2.41},
                {'age':60, 'rate':4.72}
                ]
            #I want to choose the first key value that is greater than a value that I am comparing
            res = list(filter(lambda edad:edad['age']<=x['age'], rate))
            print(res[-1]['rate'])
            # Go through each plan of each client
            for y in x['planes']:
                value = (y['coverage']/1000)*res[-1]['rate']*0.1 + y['deducible']/100
                profit.append(value)
            x['profit'] = sum(profit)   
        return Response({'customers':sorted_q})
       
# Get Customer
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def customer(request, contact_id):
    if request.method == 'GET':
        try:
            contact = Contact.objects.get(id = contact_id)
            customer = Customer.objects.get(contacto = contact_id)
            print(customer.planes.all())
            plans = customer.planes.all()
            serializerplans = PlanSeguroSerializer(plans, context={'request': request}, many= True)
            information = []
            information.append({'name':contact.name, 'phone':contact.phone, 'email':contact.email})
            serializer = GetCustomerSerializer(customer, context={'request': request})
            return Response({'customer':serializer.data, 'information': information, 'plans':serializerplans.data})
        except Contact.DoesNotExist:
            return JsonResponse({"error": "Contact not exist."}, status=404)
        except Customer.DoesNotExist:
            return JsonResponse({"error": "Customer not exist."}, status=404)

# Edit and delete contact
@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def edit_contact(request, contact_id):
    try:
        contact = Contact.objects.get(id = contact_id)
    except Contact.DoesNotExist:
        return JsonResponse({"error": "Contact not exist."}, status=404)
    
    if request.method == 'PUT':
        serializer = ContactSerializer(contact, data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        contact.delete()
        return Response({'delete':'Contact deleted'})

#Edit and delete customer
@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def edit_customer(request, customer_id):
    try:
        customer = Customer.objects.get(id = customer_id)
        id = customer.contacto.id
        contact = Contact.objects.get(id = id)
    except Customer.DoesNotExist:
        return JsonResponse({"error": "Customer not exist."}, status=404)
    
    if request.method == 'PUT':
        serializer = CustomerSerializer(customer, data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        contact.iscustomer = False
        contact.save()
        customer.delete()
        return Response({'delete':'Customer deleted'})

# Get all plans of a certain plan
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def related_plans(request, username_id):
    # Get plans and customers
    if request.method == 'GET':
        user = User.objects.filter(id = username_id).first()
        contacts = user.creador.all()
        planes = []
        duplas = []
        data = []
        for contact in contacts:
            customer = contact.info_contact.all().first()
            if customer !=None:
                planes_customer = customer.planes.all()
                for plan in planes_customer:
                    planes.append(plan.plan)
        for x in planes:
            resultado = list(filter(lambda y : y == x, planes))
            value = ({"plan": x, "customers":len(resultado)})
            duplas.append(value) 
        # Remove duplicate values  
        [data.append(z) for z in duplas if z not in data]
        print(data)
        # Sort from highest to lowest
        data_sorted = sorted(data, key=lambda x: x['customers'], reverse=True)
        return JsonResponse({'plans_customers':data_sorted}, status=200)

@api_view(['GET'])
def mensaje(request):
    if request.method == 'GET':
        return JsonResponse({'message': 'Hola este es el API de insurances'})