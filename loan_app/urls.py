from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'customers', views.CustomerViewSet)
router.register(r'loans', views.LoanViewSet)


urlpatterns = [
        path('', include(router.urls)),
        path('transaction-data/', views.TransactionDataView.as_view()),
    ]