from rest_framework.serializers import ModelSerializer
from rest_framework import fields, serializers
from .models import User, Contact, PlanSeguro, Customer

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'last_login', 'date_joined')

class ContactSerializer(ModelSerializer):
    class Meta:
        model = Contact
        fields = ('id', 'name', 'phone', 'email', 'creador')

class GetContactSerializer(ModelSerializer):
    timestamp = fields.DateTimeField()
    class Meta:
        model = Contact
        fields = ['id', 'name', 'phone', 'email', 'timestamp', 'iscustomer', 'creador']

class PlanSeguroSerializer(ModelSerializer):
    class Meta:
        model = PlanSeguro
        fields = ('id', 'plan', 'coverage', 'deducible', 'company')

class CustomerSerializer(serializers.ModelSerializer):
    #planes = PlanSeguroSerializer(many=True, read_only=True)
    class Meta:
        model = Customer
        fields = ['id', 'contacto', 'planes', 'timecustomer', 'payment', 'age']

class GetCustomerSerializer(serializers.ModelSerializer):
    contacto = serializers.CharField(source='contacto.name')
    planes = PlanSeguroSerializer(many=True, read_only=True)
    class Meta:
        model = Customer
        fields = ['id', 'contacto', 'planes', 'timecustomer', 'payment', 'age']