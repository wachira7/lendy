import requests

from zeep import Client
from django.conf import settings
from decouple import config
from celery import shared_task

from loan_app.models import Loan



class CoreBankingAPIClient:
    def __init__(self):
        self.kyc_wsdl = config("CORE_BANKING_KYC_WSDL")
        self.transaction_wsdl = config("CORE_BANKING_TRANSACTION_WSDL")
        self.username = config("CORE_BANKING_USERNAME")
        self.password = config("CORE_BANKING_PASSWORD")

    def get_customer_kyc(self, customer_number):
        response = requests.get(f"{self.kyc_wsdl}/{customer_number}")
        return response.json() if response.status_code == 200 else None

class CoreBankingService:
    def __init__(self):
        self.client = CoreBankingAPIClient()

    def get_customer_kyc(self, customer_number):
        return self.client.get_customer_kyc(customer_number)

class ScoringEngineService:
    def initiate_query_score(self, customer_number):
        return f"token_{customer_number}"  # Placeholder token, replaced in prod

    @shared_task
    def get_score_and_limit_with_retry(loan_id, token):
        loan = Loan.objects.get(id=loan_id)
        loan.status = 'APPROVED'  # Simulated scoring approval,
        loan.save()