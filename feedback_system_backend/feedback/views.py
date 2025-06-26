from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView

from django.contrib.auth import get_user_model

from .models import Feedback, User
from .serializers import (
    FeedbackSerializer,
    UserSignupSerializer,
    EmployeeListSerializer,
    UserSerializer
)

User = get_user_model()


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Feedback.objects.all()

        if user.role == 'manager':
            queryset = queryset.filter(manager=user)
            emp_id = self.request.query_params.get('employee')
            if emp_id:
                queryset = queryset.filter(employee__id=emp_id)
            return queryset

        return Feedback.objects.filter(employee=user)

    def perform_create(self, serializer):
        user = self.request.user
        if user.role != 'manager':
            raise ValidationError("Only managers can create feedback.")

        employee_id = self.request.data.get('employee')
        try:
            employee = User.objects.get(id=employee_id, role='employee')
        except User.DoesNotExist:
            raise ValidationError({'employee': 'Invalid employee ID'})

        instance = serializer.save(manager=user, employee=employee)
        print(" Feedback saved successfully:", instance)

    @action(detail=False, methods=['get'], url_path='my-feedbacks')
    def my_feedbacks(self, request):
        user = request.user
        feedbacks = Feedback.objects.filter(employee=user)
        serializer = self.get_serializer(feedbacks, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'], url_path='acknowledge')
    def acknowledge(self, request, pk=None):
        feedback = self.get_object()
        if feedback.employee != request.user:
            return Response({"detail": "Not allowed."}, status=status.HTTP_403_FORBIDDEN)
        feedback.acknowledged = True
        feedback.save()
        return Response({'status': 'acknowledged'})

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user != instance.manager:
            return Response({"detail": "Not allowed."}, status=status.HTTP_403_FORBIDDEN)
        return super().partial_update(request, *args, **kwargs)


class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSignupSerializer
    permission_classes = [permissions.AllowAny]


class CustomLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'username': user.username,
            'role': user.role,
        })


class EmployeeListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        employees = User.objects.filter(role='employee')
        serializer = EmployeeListSerializer(employees, many=True)
        return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        role = self.request.query_params.get('role')
        if role:
            return User.objects.filter(role=role)
        return User.objects.all()
