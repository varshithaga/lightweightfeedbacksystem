from rest_framework.routers import DefaultRouter
from .views import FeedbackViewSet
from .views import FeedbackViewSet, SignupView, CustomLoginView ,EmployeeListView,UserViewSet 
from django.urls import path, include

router = DefaultRouter()
router.register(r'feedbacks', FeedbackViewSet, basename='feedback')  
router.register(r'users', UserViewSet, basename='user')  

urlpatterns = [
    path('', include(router.urls)),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('users/', EmployeeListView.as_view(), name='employee-list'),  
]