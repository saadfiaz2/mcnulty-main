from django.urls import path, include
from .views import LoginView
from .views import  ReasonListView, RecordListView, AgentListView
from rest_framework.routers import DefaultRouter

# Initialize the router
router = DefaultRouter()
router.register(r'records', RecordListView)
router.register(r'agents', AgentListView)
router.register(r'reasons', ReasonListView)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'), 
]