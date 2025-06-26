from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import Feedback, User

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'role']

class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'password', 'role', 'email']

    def validate_username(self, value):
        role = self.initial_data.get('role')

        if role == 'manager' and not value.endswith('@manager'):
            raise serializers.ValidationError("Manager username must end with '@manager'")
        elif role == 'employee' and not value.endswith('@employee'):
            raise serializers.ValidationError("Employee username must end with '@employee'")
        return value

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            role=validated_data['role'],
            password=validated_data['password']
        )

class FeedbackSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.username', read_only=True)
    manager_name = serializers.CharField(source='manager.username', read_only=True)
    manager = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Feedback
        fields = [
            'id', 'employee', 'employee_name',
            'manager', 'manager_name',
            'strengths', 'areas_to_improve',
            'sentiment', 'acknowledged', 'created_at'
        ]
        read_only_fields = ['manager', 'acknowledged', 'created_at']

class EmployeeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
